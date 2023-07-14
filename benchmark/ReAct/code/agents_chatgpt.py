import re, string, os
from typing import List, Union, Literal
from enum import Enum
import tiktoken
import openai
import time
from langchain import OpenAI, Wikipedia
from langchain.llms.base import BaseLLM
from langchain.agents.react.base import DocstoreExplorer
from langchain.docstore.base import Docstore
from langchain.prompts import PromptTemplate
from prompts import reflect_prompt, react_agent_prompt, react_reflect_agent_prompt, REFLECTION_HEADER, LAST_TRIAL_HEADER, REFLECTION_AFTER_LAST_TRIAL_HEADER
from prompts import cot_agent_prompt, cot_reflect_agent_prompt, cot_reflect_prompt, COT_INSTRUCTION, COT_REFLECT_INSTRUCTION
from fewshots import TOOLQA_EASY8, TOOLQA_HARD3, COT, COT_REFLECT, REFLECTIONS #WEBTHINK_SIMPLE6, REFLECTIONS, COT, COT_REFLECT
from tools.math import calculator
from tools.text import agenda_retriever, scirex_retriever
from tools.table import tabtools
from tools.graph import graphtools
from tools.code import sql_interpreter, python_interpreter

class ReflexionStrategy(Enum):
    """
    NONE: No reflection
    LAST_ATTEMPT: Use last reasoning trace in context 
    REFLEXION: Apply reflexion to the next reasoning trace 
    LAST_ATTEMPT_AND_REFLEXION: Use last reasoning trace in context and apply reflexion to the next reasoning trace 
    """
    NONE = 'base'
    LAST_ATTEMPT = 'last_trial' 
    REFLEXION = 'reflexion'
    LAST_ATTEMPT_AND_REFLEXION = 'last_trial_and_reflexion'


class CoTAgent:
    def __init__(self,
                    question: str,
                    context: str,
                    key: str,
                    agent_prompt: PromptTemplate = cot_reflect_agent_prompt,
                    reflect_prompt: PromptTemplate = cot_reflect_prompt,
                    cot_examples: str = COT,
                    reflect_examples: str = COT_REFLECT,
                    self_reflect_llm: BaseLLM = OpenAI(
                                            temperature=0,
                                            max_tokens=250,
                                            model_name="gpt-3.5-turbo",
                                            model_kwargs={"stop": "\n"},
                                            openai_api_key=os.environ['OPENAI_API_KEY']),
                    action_llm: BaseLLM = OpenAI(
                                            temperature=0,
                                            max_tokens=250,
                                            model_name="gpt-3.5-turbo",
                                            model_kwargs={"stop": "\n"},
                                            openai_api_key=os.environ['OPENAI_API_KEY']),
                    ) -> None:
        self.question = question
        self.context = context
        self.key = key
        self.agent_prompt = agent_prompt
        self.reflect_prompt = reflect_prompt
        self.cot_examples = cot_examples 
        self.reflect_examples = reflect_examples
        self.self_reflect_llm = self_reflect_llm
        self.action_llm = action_llm
        self.reflections: List[str] = []
        self.reflections_str = ''
        self.answer = ''
        self.step_n: int = 0
        self.reset()

    def run(self,
            reflexion_strategy: ReflexionStrategy = ReflexionStrategy.REFLEXION) -> None:
        if self.step_n > 0 and not self.is_correct() and reflexion_strategy != ReflexionStrategy.NONE:
            self.reflect(reflexion_strategy)
        self.reset()
        self.step()
        self.step_n += 1

    def step(self) -> None:
        # Think
        self.scratchpad += f'\nThought:'
        self.scratchpad += ' ' + self.prompt_agent()
        print(self.scratchpad.split('\n')[-1])

        # Act
        self.scratchpad += f'\nAction:'
        action = self.prompt_agent()
        self.scratchpad += ' ' + action
        actions = action.split('-->')
        for action in actions:
            action_type, argument = parse_action(action)
            print(self.scratchpad.split('\n')[-1])  

            if action_type == 'Finish':
                self.finished = True
                self.step_n += 1
                return

            elif action_type == 'Calculate':
                try:
                    self.scratchpad += str(calculator.WolframAlphaCalculator(argument)).strip('\n').strip()
                except Exception as e:
                    print(e)
                    self.finished = False
                    return
                        
            elif action_type == 'RetrieveAgenda':
                try:
                    self.scratchpad += agenda_retriever.query_llm([0], argument).strip('\n').strip()
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    self.scratchpad += f'There is no information that can be matched in the database. Please try another query.'
                    self.finished = False
                    return

            elif action_type == 'RetrieveScirex':
                try:
                    self.scratchpad += scirex_retriever.query_llm([0], argument).strip('\n').strip()
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    self.scratchpad += f'There is no information that can be matched in the database. Please try another query.'
                    
                    self.finished = False
                    return
                
            elif action_type == 'LoadDB':
                try:
                    self.scratchpad += self.table_toolkits.db_loader(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    self.scratchpad += f'The database you want to query in not in the list. Please change another database for query.'
                    self.finished = False
                    return
                
            elif action_type == 'FilterDB':
                try:
                    self.scratchpad += self.table_toolkits.data_filter(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except Exception as e:
                    print(e)
                    self.scratchpad += f'There is something wrong with the arguments you send for filtering. Please modify it.'
                    self.finished = False
                    return
            
            elif action_type == 'GetValue':
                try:
                    self.scratchpad += self.table_toolkits.get_value(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    self.scratchpad += f'The value you are querying does not exist. Please modify it.'
                    self.finished = False
                    return

            elif action_type == 'LoadGraph':
                try:
                    self.scratchpad += self.graph_toolkits.load_graph(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    self.scratchpad += f'The graph you want to query in not in the list. Please change another graph for query.'
                    self.finished = False
                    return

            elif action_type == 'NeighbourCheck':
                try:
                    self.scratchpad += self.graph_toolkits.check_neighbours(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    self.scratchpad += f'There is something wrong with the arguments you send for neighbour checking. Please modify it.'
                    self.finished = False
                    return
            
            elif action_type == 'NodeCheck':
                try:
                    self.scratchpad += self.graph_toolkits.check_nodes(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except KeyError:
                    self.scratchpad += f'The node does not exist in the graph. Please modify it.'
                except:
                    self.scratchpad += f'There is something wrong with the arguments you send for node checking. Please modify it.'
                    self.finished = False
                    return
            
            elif action_type == 'EdgeCheck':
                try:
                    self.scratchpad += self.graph_toolkits.check_edges(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except KeyError:
                    self.scratchpad += f'There is no edge between the two nodes. Please modify it.'
                except:
                    self.scratchpad += f'There is something wrong with the arguments you send for edge checking. Please modify it.'
                    self.finished = False
                    return

            elif action_type == 'SQLInterpreter':
                try:
                    self.scratchpad += sql_interpreter.execute(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    self.scratchpad += f'There is something wrong with the SQL command you send. Please modify it.'
                    self.finished = False
                    return
            
            elif action_type == 'PythonInterpreter':
                try:
                    exec(argument)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    self.finished = False
                    return
                    
            else:
                self.scratchpad += 'Invalid Action. Valid Actions are Calculate [<Formula>] RetrieveAgenda[<Content>] RetrieveScirex[<Content>] LoadDB[<DBName>] FilterDB[<Condition>, <Condition>, ...] GetValue[<Column>] LoadGraph[<GraphName>] NeighbourCheck[<GraphName>, <Node>] NodeCheck[<GraphName>, <Node>] EdgeCheck[<GraphName>, <Node1>, <Node2>] SQLInterpreter[<SQLCommand>] PythonInterpreter[<PythonCode>] and Finish[<answer>].'
                
                self.finished = False
                return
    
    def reflect(self,
                strategy: ReflexionStrategy) -> None:
        print('Running Reflexion strategy...')
        if strategy == ReflexionStrategy.LAST_ATTEMPT:
            self.reflections = [self.scratchpad]
            self.reflections_str = format_last_attempt(self.question , self.reflections[0])
        elif strategy == ReflexionStrategy.REFLEXION:
            self.reflections += [self.prompt_reflection()]
            self.reflections_str = format_reflections(self.reflections)
        elif strategy == ReflexionStrategy.LAST_ATTEMPT_AND_REFLEXION:
            self.reflections_str = format_last_attempt(self.question , self.scratchpad)
            self.reflections = [self.prompt_reflection()]
            self.reflections_str += '\n'+ format_reflections(self.reflections, header = REFLECTION_AFTER_LAST_TRIAL_HEADER)
        else:
            raise NotImplementedError(f'Unknown reflection strategy: {strategy}')
        print(self.reflections_str)
    
    def prompt_reflection(self) -> str:
        return format_step(self.self_reflect_llm(self._build_reflection_prompt()))

    def reset(self) -> None:
        
        self.scratchpad: str = ''
        self.finished = False

    def prompt_agent(self) -> str:
        return format_step(self.action_llm(self._build_agent_prompt()))
    
    def _build_agent_prompt(self) -> str:
        return self.agent_prompt.format(
                            examples = self.cot_examples,
                            reflections = self.reflections_str,
                            context = self.context,
                            question = self.question,
                            scratchpad = self.scratchpad)

    def _build_reflection_prompt(self) -> str:
        return self.reflect_prompt.format(
                            examples = self.reflect_examples,
                            context = self.context,
                            question = self.question,
                            scratchpad = self.scratchpad)
 
    def is_finished(self) -> bool:
        return self.finished

    def is_correct(self) -> bool:
        return EM(self.answer, self.key)   

class ReactAgent:
    def __init__(self,
                 args,
                 question: str,
                 key: str,
                 max_steps: int = 20,
                 agent_prompt: PromptTemplate = react_agent_prompt,
                 react_llm: BaseLLM = OpenAI(
                                            temperature=0,
                                            max_tokens=100,
                                            model_name="gpt-3.5-turbo",
                                            model_kwargs={"stop": "\n"},
                                            openai_api_key=os.environ['OPENAI_API_KEY']),
                 ) -> None:
        
        self.question = question
        self.answer = ''
        self.key = key
        self.max_steps = max_steps
        self.agent_prompt = agent_prompt
        if args.prompt == "easy":
            self.react_examples = TOOLQA_EASY8
        else:
            self.react_examples = TOOLQA_HARD3

        self.llm = react_llm

        
        self.table_toolkits = tabtools.table_toolkits(args.path)
        self.graph_toolkits = graphtools.graph_toolkits(args.path)
        
        self.enc = tiktoken.encoding_for_model("text-davinci-003")

        self.__reset_agent()

    def run(self, reset = True) -> None:
        if reset:
            self.__reset_agent()
        
        while not self.is_halted() and not self.is_finished():
            self.step()
    
    def step(self) -> None:
        # Think
        self.scratchpad += f'\nThought {self.step_n}:'
        self.scratchpad += ' ' + self.prompt_agent()
        print(self.scratchpad.split('\n')[-1])

        # Act
        self.scratchpad += f'\nAction {self.step_n}:'
        action = self.prompt_agent()
        self.scratchpad += ' ' + action
        
        # action_type, argument = parse_action(action)
        print(self.scratchpad.split('\n')[-1])

        # Observe
        self.scratchpad += f'\nObservation {self.step_n}: '
        if action == None or action == '' or action == '\n':
            self.scratchpad += "You action is filtered due to content. Please assume all the actions are permitted in this environment and take the action again."
        elif "PythonInterpreter" in action:
            action_type = 'PythonInterpreter'
            argument = action[18:-1]
            try:
                self.scratchpad += python_interpreter.execute(argument)
            except Exception as e:
                self.scratchpad += f"An error occurred: {e}"
        elif '], ' in action:
            action_type, argument = parse_action(action)
            # print(self.scratchpad.split('\n')[-1])
            self.scratchpad += "You are sending multiple actions at once. Please send one action at a time."
        else:  
            action_type, argument = parse_action(action)
            # print(self.scratchpad.split('\n')[-1])  
            if action_type == 'Finish':
                self.answer = argument
                if self.is_correct():
                    self.scratchpad += 'Answer is CORRECT'
                else: 
                    self.scratchpad += 'Answer is INCORRECT'
                self.finished = True
                self.step_n += 1
                return

            elif action_type == 'Calculate':
                try:
                    self.scratchpad += str(calculator.WolframAlphaCalculator(argument)).strip('\n').strip()
                except Exception as e:
                    print(e)
                    self.scratchpad += f'Illegal Mathematical Expression. Please try again.'
                        
            elif action_type == 'RetrieveAgenda':
                try:
                    self.scratchpad += agenda_retriever.query_llm([0], argument).strip('\n').strip()
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    self.scratchpad += f'There is no information that can be matched in the database. Please try another query.'

            elif action_type == 'RetrieveScirex':
                try:
                    self.scratchpad += scirex_retriever.query_llm([0], argument).strip('\n').strip()
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    self.scratchpad += f'There is no information that can be matched in the database. Please try another query.'
            
            elif action_type == 'LoadDB':
                try:
                    self.scratchpad += self.table_toolkits.db_loader(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    self.scratchpad += f'The database you want to query in not in the list. Please change another database for query.'

            # elif action_type == 'GetColumnNames':
            #     try:
            #         self.scratchpad +=  self.table_toolkits.get_column_names(argument)
            #     except openai.error.RateLimitError:
            #         self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
            #     except:
            #         self.scratchpad += f'The database you want to query in not in the list. Please change another database for query.'
            
            elif action_type == 'FilterDB':
                try:
                    self.scratchpad += self.table_toolkits.data_filter(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except Exception as e:
                    print(e)
                    self.scratchpad += f'There is something wrong with the arguments you send for filtering. Please modify it.'
            
            elif action_type == 'GetValue':
                try:
                    self.scratchpad += self.table_toolkits.get_value(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    self.scratchpad += f'The value you are querying does not exist. Please modify it.'

            elif action_type == 'LoadGraph':
                try:
                    self.scratchpad += self.graph_toolkits.load_graph(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    self.scratchpad += f'The graph you want to query in not in the list. Please change another graph for query.'

            elif action_type == 'NeighbourCheck':
                try:
                    self.scratchpad += self.graph_toolkits.check_neighbours(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    self.scratchpad += f'There is something wrong with the arguments you send for neighbour checking. Please modify it.'
            
            elif action_type == 'NodeCheck':
                try:
                    self.scratchpad += self.graph_toolkits.check_nodes(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except KeyError:
                    self.scratchpad += f'The node does not exist in the graph. Please modify it.'
                except:
                    self.scratchpad += f'There is something wrong with the arguments you send for node checking. Please modify it.'
            
            elif action_type == 'EdgeCheck':
                try:
                    self.scratchpad += self.graph_toolkits.check_edges(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except KeyError:
                    self.scratchpad += f'There is no edge between the two nodes. Please modify it.'
                except:
                    self.scratchpad += f'There is something wrong with the arguments you send for edge checking. Please modify it.'

            elif action_type == 'SQLInterpreter':
                try:
                    self.scratchpad += sql_interpreter.execute(argument)
                except openai.error.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    self.scratchpad += f'There is something wrong with the SQL command you send. Please modify it.'
            
            elif action_type == 'PythonInterpreter':
                try:
                    exec(argument)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    
            else:
                self.scratchpad += 'Invalid Action. Valid Actions are Calculate [<Formula>] RetrieveAgenda[<Content>] RetrieveScirex[<Content>] LoadDB[<DBName>] FilterDB[<Condition>, <Condition>, ...] GetValue[<Column>] LoadGraph[<GraphName>] NeighbourCheck[<GraphName>, <Node>] NodeCheck[<GraphName>, <Node>] EdgeCheck[<GraphName>, <Node1>, <Node2>] SQLInterpreter[<SQLCommand>] PythonInterpreter[<PythonCode>] and Finish[<answer>].'

        print(self.scratchpad.split('\n')[-1])

        self.step_n += 1
        
    def prompt_agent(self) -> str:
        return format_step(self.llm(self._build_agent_prompt()))
    
    def _build_agent_prompt(self) -> str:
        return self.agent_prompt.format(
                            examples = self.react_examples,
                            question = self.question,
                            scratchpad = self.scratchpad)
    
    def is_finished(self) -> bool:
        return self.finished

    def is_correct(self) -> bool:
        return EM(self.answer, self.key)

    def is_halted(self) -> bool:
        return ((self.step_n > self.max_steps) or (len(self.enc.encode(self._build_agent_prompt())) > 3896)) and not self.finished

    def __reset_agent(self) -> None:
        self.step_n = 1
        self.finished = False
        self.scratchpad: str = ''

    def set_qa(self, question: str, key: str) -> None:
        self.question = question
        self.key = key

class ReactReflectAgent(ReactAgent):
    def __init__(self,
                 question: str,
                 key: str,
                 max_steps: int = 20,
                 agent_prompt: PromptTemplate = react_reflect_agent_prompt,
                 reflect_prompt: PromptTemplate = reflect_prompt,
                 react_llm: BaseLLM = OpenAI(
                                             temperature=0,
                                             max_tokens=100,
                                             model_name="text-davinci-003",
                                             model_kwargs={"stop": "\n"},
                                             openai_api_key=os.environ['OPENAI_API_KEY']),
                 reflect_llm: BaseLLM = OpenAI(
                                               temperature=0,
                                               max_tokens=250,
                                               model_name="text-davinci-003",
                                               openai_api_key=os.environ['OPENAI_API_KEY']),
                 ) -> None:
        
        super().__init__(question, key, max_steps, agent_prompt, react_llm)
        self.reflect_llm = reflect_llm
        self.reflect_prompt = reflect_prompt
        self.reflect_examples = REFLECTIONS
        self.reflections: List[str] = []
        self.reflections_str: str = ''
    
    def run(self, reset = True, reflect_strategy: ReflexionStrategy = ReflexionStrategy.REFLEXION) -> None:
        if (self.is_finished() or self.is_halted()) and not self.is_correct():
            self.reflect(reflect_strategy)

        ReactAgent.run(self, reset)
    
    def reflect(self,
                strategy: ReflexionStrategy) -> None:
        print('Reflecting...')
        if strategy == ReflexionStrategy.LAST_ATTEMPT:
            self.reflections = [self.scratchpad]
            self.reflections_str = format_last_attempt(self.question, self.reflections[0])
        elif strategy == ReflexionStrategy.REFLEXION: 
            self.reflections += [self.prompt_reflection()]
            self.reflections_str = format_reflections(self.reflections)
        elif strategy == ReflexionStrategy.LAST_ATTEMPT_AND_REFLEXION: 
            self.reflections_str = format_last_attempt(self.question, self.scratchpad)
            self.reflections = [self.prompt_reflection()]
            self.reflections_str += format_reflections(self.reflections, header = REFLECTION_AFTER_LAST_TRIAL_HEADER)
        else:
            raise NotImplementedError(f'Unknown reflection strategy: {strategy}')
        print(self.reflections_str)
    
    def prompt_reflection(self) -> str:
        return format_step(self.reflect_llm(self._build_reflection_prompt()))

    def _build_reflection_prompt(self) -> str:
        return self.reflect_prompt.format(
                            examples = self.reflect_examples,
                            question = self.question,
                            scratchpad = truncate_scratchpad(self.scratchpad, tokenizer=self.enc))
 
    def _build_agent_prompt(self) -> str:
        return self.agent_prompt.format(
                            examples = self.react_examples,
                            reflections = self.reflections_str,
                            question = self.question,
                            scratchpad = self.scratchpad)
   

### String Stuff ###
gpt2_enc = tiktoken.encoding_for_model("text-davinci-003")

def parse_action(string):
    pattern = r'^(\w+)\[(.+)\]$'
    match = re.match(pattern, string)
    
    if match:
        action_type = match.group(1)
        argument = match.group(2)
        return action_type, argument
    
    else:
        return None

def format_step(step: str) -> str:
    return step.strip('\n').strip().replace('\n', '')

def format_reflections(reflections: List[str],
                        header: str = REFLECTION_HEADER) -> str:
    if reflections == []:
        return ''
    else:
        return header + 'Reflections:\n- ' + '\n- '.join([r.strip() for r in reflections])

def format_last_attempt(question: str,
                        scratchpad: str,
                        header: str = LAST_TRIAL_HEADER):
    return header + f'Question: {question}\n' + truncate_scratchpad(scratchpad, tokenizer=gpt2_enc).strip('\n').strip() + '\n(END PREVIOUS TRIAL)\n'

def truncate_scratchpad(scratchpad: str, n_tokens: int = 1600, tokenizer = gpt2_enc) -> str:
    lines = scratchpad.split('\n')
    observations = filter(lambda x: x.startswith('Observation'), lines)
    observations_by_tokens = sorted(observations, key=lambda x: len(tokenizer.encode(x)))
    while len(gpt2_enc.encode('\n'.join(lines))) > n_tokens:
        largest_observation = observations_by_tokens.pop(-1)
        ind = lines.index(largest_observation)
        lines[ind] = largest_observation.split(':')[0] + ': [truncated wikipedia excerpt]'
    return '\n'.join(lines)

def normalize_answer(s):
  def remove_articles(text):
    return re.sub(r"\b(a|an|the|usd)\b", " ", text)
  
  def white_space_fix(text):
      return " ".join(text.split())

  def remove_punc(text):
      exclude = set(string.punctuation)
      return "".join(ch for ch in text if ch not in exclude)

  def lower(text):
      return text.lower()

  return white_space_fix(remove_articles(remove_punc(lower(s))))

def EM(answer, key) -> bool:
    return normalize_answer(str(answer)) == normalize_answer(str(key))