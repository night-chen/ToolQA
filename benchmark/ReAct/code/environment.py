import re
import string
from typing import Tuple

import gym
import openai
from tools.math import calculator
from tools.text import agenda_retriever, scirex_retriever
from tools.table import tabtools
from tools.graph import graphtools
from tools.code import sql_interpreter, python_interpreter
class QAEnv(gym.Env):
    def __init__(self,
                 question: str,
                 key: str,
                 max_steps: int = 20):
        
        self.question = question
        self.key = key
        self.max_steps = max_steps
        self.table_toolkits = tabtools.table_toolkits("<YOUR_OWN_PATH>")
        self.graph_toolkits = graphtools.graph_toolkits("<YOUR_OWN_PATH>")

        self.reset()

    def reset(self):
          self.curr_step = 0
          self.terminated = False
          self.answer = ''

    def step(self, action: str) -> Tuple[str, bool, bool, bool, bool]:
        if action == None or action == '' or action == '\n':
            observation = "You action is filtered due to content. Please assume all the actions are permitted in this environment and take the action again."
        elif "PythonInterpreter" in action:
            action_type = 'PythonInterpreter'
            argument = action[18:-1]
            try:
                observation = python_interpreter.execute(argument)
            except Exception as e:
                observation = f"An error occurred: {e}"
        elif '], ' in action:
            observation = "You are sending multiple actions at once. Please send one action at a time."
        else:
            action_type, argument = parse_action(action)

            if action_type == 'Finish':
                self.answer = argument
                if self.is_correct():
                    observation = 'Answer is CORRECT'
                else: 
                    observation = 'Answer is INCORRECT'
                self.terminated = True

            elif action_type == 'Calculate':
                try:
                    observation = str(calculator.WolframAlphaCalculator(argument)).strip('\n').strip()
                except Exception as e:
                    print(e)
                    observation = f'Illegal Mathematical Expression. Please try again.'
                        
            elif action_type == 'RetrieveAgenda':
                try:
                    observation = agenda_retriever.query_llm([0], argument).strip('\n').strip()
                except openai.error.RateLimitError:
                    observation = f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    observation = f'There is no information that can be matched in the database. Please try another query.'

            elif action_type == 'RetrieveScirex':
                try:
                    observation = scirex_retriever.query_llm([0], argument).strip('\n').strip()
                except openai.error.RateLimitError:
                    observation = f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    observation = f'There is no information that can be matched in the database. Please try another query.'
            
            elif action_type == 'LoadDB':
                try:
                    observation = self.table_toolkits.db_loader(argument)
                except openai.error.RateLimitError:
                    observation = f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    observation = f'The database you want to query in not in the list. Please change another database for query.'

            # elif action_type == 'GetColumnNames':
            #     try:
            #         observation = self.table_toolkits.get_column_names(argument)
            #     except openai.error.RateLimitError:
            #         observation = f'OpenAI API Rate Limit Exceeded. Please try again.'
            #     except:
            #         observation = f'The database you want to query in not in the list. Please change another database for query.'
            
            elif action_type == 'FilterDB':
                try:
                    observation = self.table_toolkits.data_filter(argument)
                except openai.error.RateLimitError:
                    observation = f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    observation = f'There is something wrong with the arguments you send for filtering. Please modify it.'
            
            elif action_type == 'GetValue':
                try:
                    observation = self.table_toolkits.get_value(argument)
                except openai.error.RateLimitError:
                    observation = f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    observation = f'The value you are querying does not exist. Please modify it.'

            elif action_type == 'LoadGraph':
                try:
                    observation = self.graph_toolkits.graph_loader(argument)
                except openai.error.RateLimitError:
                    observation = f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    observation = f'The graph you want to query in not in the list. Please change another graph for query.'

            elif action_type == 'NeighbourCheck':
                try:
                    observation = self.graph_toolkits.neighbour_check(argument)
                except openai.error.RateLimitError:
                    observation = f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    observation = f'There is something wrong with the arguments you send for neighbour checking. Please modify it.'
            
            elif action_type == 'NodeCheck':
                try:
                    observation = self.table_toolkits.check_nodes(argument)
                except openai.error.RateLimitError:
                    observation = f'OpenAI API Rate Limit Exceeded. Please try again.'
                except KeyError:
                    observation = f'The node does not exist in the graph. Please modify it.'
                except:
                    observation = f'There is something wrong with the arguments you send for node checking. Please modify it.'
            
            elif action_type == 'EdgeCheck':
                try:
                    observation = self.table_toolkits.check_edges(argument)
                except openai.error.RateLimitError:
                    observation = f'OpenAI API Rate Limit Exceeded. Please try again.'
                except KeyError:
                    observation = f'There is no edge between the two nodes. Please modify it.'
                except:
                    observation = f'There is something wrong with the arguments you send for edge checking. Please modify it.'

            elif action_type == 'SQLInterpreter':
                try:
                    observation = sql_interpreter.execute(argument)
                except openai.error.RateLimitError:
                    observation = f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    observation = f'There is something wrong with the SQL command you send. Please modify it.'
            
            elif action_type == "PythonInterpreter":
                action_type = 'PythonInterpreter'
                argument = action[18:-1]
                try:
                    observation = python_interpreter.execute(argument)
                except Exception as e:
                    observation = f"An error occurred: {e}"
                    
            else:
                observation = 'Invalid Action. Valid Actions are Calculate [<Formula>] RetrieveAgenda[<Content>] RetrieveScirex[<Content>] LoadDB[<DBName>] FilterDB[<Condition>, <Condition>, ...] GetValue[<Column>] LoadGraph[<GraphName>] NeighbourCheck[<GraphName>, <Node>] NodeCheck[<GraphName>, <Node>] EdgeCheck[<GraphName>, <Node1>, <Node2>] SQLInterpreter[<SQLCommand>] PythonInterpreter[<PythonCode>] and Finish[<answer>].'

        reward = self.is_correct()
        terminated = self.is_terminated()
        truncated = self.is_truncated()

        self.curr_step += 1

        return observation, reward, terminated, truncated, self.curr_step

    def is_correct(self) -> bool:
        return EM(self.answer, self.key)
    
    def is_terminated(self) -> bool:
        return self.terminated

    def is_truncated(self) -> bool:
        return self.curr_step >= self.max_steps

def parse_action(string):
    pattern = r'^(\w+)\[(.+)\]$'
    match = re.match(pattern, string)
    
    if match:
        action_type = match.group(1)
        argument = match.group(2)
        return action_type, argument
    
    else:
        return None, None

def normalize_answer(s):
  def remove_articles(text):
    return re.sub(r"\b(a|an|the|USD)\b", " ", text)
  
  def white_space_fix(text):
      return " ".join(text.split())

  def remove_punc(text):
      exclude = set(string.punctuation)
      return "".join(ch for ch in text if ch not in exclude)

  def lower(text):
      return text.lower()

  return white_space_fix(remove_articles(remove_punc(lower(s))))

def EM(answer, key) -> bool:
    return normalize_answer(answer) == normalize_answer(key)