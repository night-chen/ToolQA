'''
input: formula strings
output: the answer of the mathematical formula
'''
import os
import re
from operator import pow, truediv, mul, add, sub
import wolframalpha
query = '1+2*3'

def calculator(query: str):
    operators = {
        '+': add,
        '-': sub,
        '*': mul,
        '/': truediv,
    }
    query = re.sub(r'\s+', '', query)
    if query.isdigit():
        return float(query)
    for c in operators.keys():
        left, operator, right = query.partition(c)
        if operator in operators:
            return round(operators[operator](calculator(left), calculator(right)),2)

def WolframAlphaCalculator(input_query: str):
    wolfram_alpha_appid = "YOUR_WOLFRAMALPHA_APPID"
    wolfram_client = wolframalpha.Client(wolfram_alpha_appid)
    res = wolfram_client.query(input_query)
    assumption = next(res.pods).text
    answer = next(res.results).text
    # return f"Assumption: {assumption} \nAnswer: {answer}"
    return answer

if __name__ == "__main__":
    query = 'mean(247.0, 253.0, 230.0, 264.0, 254.0, 275.0, 227.0, 258.0, 245.0, 253.0, 242.0, 229.0, 259.0, 253.0)'
    print(WolframAlphaCalculator(query))