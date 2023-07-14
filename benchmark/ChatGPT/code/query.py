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
openai.api_key = "YOUR_OPENAI_API_KEY"

from typing import List, Dict, Any
import asyncio

def clean_str(string):
    pattern = re.compile(r'^\d+\. ', flags=re.MULTILINE)
    string = pattern.sub('', string)
    return string.strip()

async def dispatch_openai_requests(
    messages_list: List[List[Dict[str, Any]]],
    model: str,
    temperature: float,
    max_tokens: int,
    top_p: float,
) -> List[str]:
    """Dispatches requests to OpenAI API asynchronously.
    
    Args:
        messages_list: List of messages to be sent to OpenAI ChatCompletion API.
        model: OpenAI model to use.
        temperature: Temperature to use for the model.
        max_tokens: Maximum number of tokens to generate.
        top_p: Top p to use for the model.
    Returns:
        List of responses from OpenAI API.
    """
    async_responses = [
        openai.ChatCompletion.acreate(
            model=model,
            messages=x,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
        for x in messages_list
    ]
    return await asyncio.gather(*async_responses)

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument("--dataset", type=str, default="flights")
    parser.add_argument("--hardness", type=str, default="easy")
    parser.add_argument("--version", type=str, default="v2")
    args = parser.parse_args()

    file_path = "/<YOUR_OWN_PATH>/ToolQA/data/questions/{}/{}-{}.jsonl".format(args.version, args.hardness, args.dataset, args.hardness)
    with open(file_path, 'r') as f:
        contents = []
        for item in jsonlines.Reader(f):
            contents.append(item)
    
    system_message = "You are an AI assistant to answer questions. Please use your own knowledge to answer the questions. If you do not know the answer, please guess a most probable answer. Only include the answer in your response. Do not explain."
    query_messages = []
    attributes = []
    for item in contents:
        message = item["question"]
        query_messages.append([
            {"role": "system", "content": system_message},
            {"role": "user", "content": message}
        ])
    generated_text = []
    for i in tqdm.trange(0, len(query_messages), 5):
        try:
            response = asyncio.run(
                dispatch_openai_requests(
                    messages_list=query_messages[i:i+5],
                    model="gpt-3.5-turbo",
                    temperature=1.0,
                    max_tokens=2048,
                    top_p=1.0,
                )
            )
            time.sleep(15)
        except:
            print("rate limit exceeded, sleep for 60 seconds")
            time.sleep(600)
            response = asyncio.run(
                dispatch_openai_requests(
                    messages_list=query_messages[i:i+5],
                    model="gpt-3.5-turbo",
                    temperature=1.0,
                    max_tokens=2048,
                    top_p=1.0,
                )
            )
        # try:
        for j in range(len(response)):
            generated_text.append({"question": contents[i+j]["question"], "model_answer": response[j]["choices"][0]["message"]["content"], "gt_answer": contents[i+j]["answer"]})
            
    
    print(generated_text[0], len(generated_text))
    output_file_path = "./results/{}/results-{}.jsonl".format(args.hardness, args.dataset)
    with jsonlines.open(output_file_path, 'w') as writer:
        for row in generated_text:
            writer.write(row)

if __name__ == '__main__':
    main()