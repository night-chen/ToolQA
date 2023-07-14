import os
import joblib
from mocks import DocStoreExplorerMock, LLMMock
import argparse
import jsonlines
from util import summarize_react_trial, log_react_trial, save_agents, remove_fewshot
import datetime

current_datetime = datetime.datetime.now()
datetime_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

# root = '{}/benchmark/ReAct/root'

parser = argparse.ArgumentParser("")
parser.add_argument("--dataset", type=str, default="flights")
parser.add_argument("--hardness", type=str, default="easy")
parser.add_argument("--openai_api_key", type=str, default="<OPENAI_API_KEY>")
parser.add_argument("--path", type=str, default="<YOUR_OWN_PATH>")
parser.add_argument("--wolframalpha_api_key", type=str, default="<WOLFALPHA_API_KEY>")
parser.add_argument("--debug", type=bool, default=False)
parser.add_argument("--debug_id", type=int, default=0)
parser.add_argument("--gpt", type=str, default="gpt3")
parser.add_argument("--prompt", type=str, default="easy")
args = parser.parse_args()
root = '{}/benchmark/ReAct/root'.format(args.path)

os.environ['OPENAI_API_KEY'] = args.openai_api_key
if args.gpt == "gpt3":
    from agents import ReactReflectAgent, ReactAgent, ReflexionStrategy
elif args.gpt == "chatgpt":
    from agents_chatgpt import ReactReflectAgent, ReactAgent, ReflexionStrategy
elif args.gpt == "azure":
    from agents_azure import ReactReflectAgent, ReactAgent, ReflexionStrategy
file_path = "{}/data/questions/{}/{}-{}.jsonl".format(args.path, args.hardness, args.dataset, args.hardness)
with open(file_path, 'r') as f:
    contents = []
    for item in jsonlines.Reader(f):
        contents.append(item)

if args.debug:
    random_indices = args.debug_id
    test_q = contents[random_indices]['question']
    test_a = contents[random_indices]['answer']
    agent = ReactAgent(args, test_q, test_a)
    agent.run()
    print(test_q)
    print(agent._build_agent_prompt())
    print("Ground-Truth: ", test_a)
else:
    if not os.path.exists('{}/benchmark/ReAct/logs/{}-{}/{}-{}'.format(args.path, args.gpt, datetime_string, args.dataset, args.hardness)):
        os.makedirs('{}/benchmark/ReAct/logs/{}-{}/{}-{}-{}'.format(args.path, args.gpt, datetime_string, args.dataset, args.hardness))
        logs_dir = '{}/benchmark/ReAct/logs/{}-{}/{}-{}-{}'.format(args.path, args.gpt, datetime_string, args.dataset, args.hardness)
    agent_cls = ReactAgent

    n = 1
    log = ''
    trial = 0
    unanswered_questions = []
    agents = []
    for i in range(len(contents)):
        agent = agent_cls(args, contents[i]['question'], contents[i]['answer'])
        try:
            agent.run()
            print(f'Answer: {agent.key}')
            print('---------')
            log = f"""
########################################
BEGIN TRIAL {contents[i]['qid']}
#######################################
"""
            log += remove_fewshot(agent._build_agent_prompt()) + f'\nCorrect answer: {agent.key}\n\n'
            with open(os.path.join(logs_dir, contents[i]['qid']+'.txt'), 'w') as f:
                f.write(log)
        except:
            print('Error when computing answer for {}.'.format(contents[i]['qid']))
            print('---------')
            log = f"""
########################################
BEGIN TRIAL {contents[i]['qid']}
#######################################
"""
            log += remove_fewshot(agent._build_agent_prompt()) + f'\nCorrect answer: {agent.key}\n\n'
            log += 'ERROR!'
            with open(os.path.join(logs_dir, contents[i]['qid']+'.txt'), 'w') as f:
                f.write(log)
            unanswered_questions.append(contents[i]['qid'])
        agents.append(agent)
    trial += 1
    log += log_react_trial(agents, trial)
    correct, incorrect, halted = summarize_react_trial(agents)
    print(f'Finished Trial {trial}, Correct: {len(correct)}, Incorrect: {len(incorrect)}, Halted: {len(halted)}')
    print('Unanswered questions: {}'.format(unanswered_questions))
    # save_agents(agents, os.path.join(root, 'ReAct', 'agents'))