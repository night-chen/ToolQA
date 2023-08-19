import os
import re
import sys
import json
import openai
from ast import literal_eval
# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utilities import *
from demos import prompt_policy

# import solvers
from tools.code.python_interpreter import execute as python_interpreter
from tools.code.sql_interpreter import execute as sql_interpreter
from tools.graph.graphtools import graph_toolkits
from tools.math.calculator import calculator, WolframAlphaCalculator
from tools.table.tabtools import table_toolkits
from tools.text.agenda_retriever import query_llm_agenda
from tools.text.scirex_retriever import query_llm_scirex
from tools import finish
import jsonlines

db = table_toolkits()
gt = graph_toolkits()
ACTION_LIST = {
    'Calculate': WolframAlphaCalculator,
    'RetrieveAgenda': query_llm_agenda,
    'RetrieveScirex': query_llm_scirex,
    'LoadDB': db.db_loader,
    'FilterDB': db.data_filter,
    'GetValue': db.get_value,
    'LoadGraph': gt.load_graph,
    'NeighbourCheck': gt.check_neighbours,
    'NodeCheck': gt.check_nodes,
    'EdgeCheck': gt.check_edges,
    'SQLInterpreter': sql_interpreter,
    'PythonInterpreter': python_interpreter,
    'Finish': finish
}

def finish(argument):
    return argument

openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)

class solver:

    def __init__(self, args):
        # arguments
        for key, value in vars(args).items():
            setattr(self, key, value)
        self.args = args
        # external arguments
        self.api_key = "<YOUR_OPENAI_API_KEY>" #openai.api_key
        self.examples, self.pids = self.load_data()
        
    def load_data(self):
        examples = ''
        pids = []
        file_path = "/<YOUR_OWN_PATH>/ToolQA/data/questions/{}/QA-{}-{}.jsonl".format(self.args.hardness, self.args.dataset, self.args.hardness)
        with open(file_path, 'r') as f:
            contents = []
            for item in jsonlines.Reader(f):
                contents.append(item)
                pids.append(item['qid'])
        examples = {item['qid']: item for item in contents}
        return examples, pids

    def build_prompt_for_policy(self):
        # demo prompt
        demo_prompt = prompt_policy.prompt_clean.strip()

        # test prompt
        question = self.cache["example"]["question"]
        # TODO: rewrite this to extract one example from the test set

        # simply for test the code
        test_prompt = f"Question: {question}\n\nModules: "

        # full prompt
        full_prompt = demo_prompt + "\n\n" + test_prompt
        return test_prompt, full_prompt

    def convert_to_executable(self, module):
        action, arg = module.split('[')
        arg = arg.rstrip(']')
        arg = arg.split(', ')
        if '=' in arg[0]:
            arg = [i.split('=')[1] for i in arg]
        return {'func_name': ACTION_LIST[action], 'args': arg}

    def update_modules(self, _modules):
        # TODO: if needed, use assert to verify the generated sequence, and give a default sequence of actions
        default_modules = _modules
        module_list = literal_eval(_modules)
        try:
            modules = [self.convert_to_executable(m) for m in module_list]

        except:
            modules = default_modules

        return modules

    def predict_modules(self):
        # get the module input
        test_prompt, full_prompt = self.build_prompt_for_policy()
        messages=[
            {"role": "user", "content": full_prompt},
        ]
        print(f'PROMPT: \n{full_prompt}\n' + '-' * 20 + '\n')
        # execute the module
        modules = get_chat_response(messages, self.api_key, self.policy_engine, self.policy_temperature, self.policy_max_tokens)
        print(f'GPT RESPONSE: \n{modules}\n')

        # modules = self.update_modules(modules)

        # update the cache
        self.cache["modules:input"] = test_prompt
        self.cache["modules:output"] = modules
        return modules
    
    