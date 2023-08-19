import jsonlines
import argparse
import tqdm
import os

import os
import re
import tqdm
import time
import requests
import json
import openai
import jsonlines
from transformers import AutoTokenizer
import transformers
import torch

from typing import List, Dict, Any
import asyncio

def clean_str(string):
    pattern = re.compile(r'^\d+\. ', flags=re.MULTILINE)
    string = pattern.sub('', string)
    return string.strip()

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument("--dataset", type=str, default="flights")
    parser.add_argument("--hardness", type=str, default="easy")
    parser.add_argument("--version", type=str, default="v2")
    args = parser.parse_args()
    model = "meta-llama/Llama-2-13b-chat-hf"
    tokenizer = AutoTokenizer.from_pretrained(model)
    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    file_path = "/<YOUR_OWN_PATH>/ToolQA/data/questions/{}/{}-{}.jsonl".format(args.hardness, args.dataset, args.hardness)
    with open(file_path, 'r') as f:
        contents = []
        for item in jsonlines.Reader(f):
            contents.append(item)
    
    system_message = "You are an AI assistant to answer questions. Please use your own knowledge to answer the questions. If you do not know the answer, please guess a most probable answer. Only include the answer in your response. Do not explain.\nQuestion: "
    query_messages = []
    attributes = []
    response = []
    for item in contents:
        message = item["question"]
        message = system_message + message + '\nAnswer:'
        msg_list = pipeline(
                        message,
                        do_sample=True,
                        top_k=10,
                        num_return_sequences=1,
                        eos_token_id=tokenizer.eos_token_id,
                        max_length=1000,
                    )
        response.append(msg_list[0]["generated_text"])

    generated_text = []
    for j in range(len(response)):
        generated_text.append({"question": contents[j]["question"], "model_answer": response[j], "gt_answer": contents[j]["answer"]})
            
    
    print(generated_text[0], len(generated_text))
    output_file_path = "./results/{}/llama-results-{}.jsonl".format(args.hardness, args.dataset)
    with jsonlines.open(output_file_path, 'w') as writer:
        for row in generated_text:
            writer.write(row)

if __name__ == '__main__':
    main()