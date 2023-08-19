import os
import time
import uuid
import numpy as np
import jsonlines
from concurrent.futures import ProcessPoolExecutor
import sentence_transformers
import chromadb
from chromadb.config import Settings

EMBED_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
CHROMA_PERSIST_DIRECTORY = "/<YOUR_OWN_PATH>/ToolQA/data/chroma_db/scirex-v2"
CHROMA_COLLECTION_NAME = "all"
CHROMA_SERVER_HOST = ""
CHROMA_SERVER_HTTP_PORT = ""
FILE_PATH = "/<YOUR_OWN_PATH>/ToolQA/data/external_corpus/scirex/Preprocessed_Scirex.jsonl"

def sentence_embedding(model, texts):
    embeddings = model.encode(texts)
    return embeddings

def create_chroma_db(chroma_server_host, chroma_server_http_port, collection_name):
    chroma_client = chromadb.Client(Settings(
        chroma_api_impl="rest",
        chroma_server_host=chroma_server_host,
        chroma_server_http_port=chroma_server_http_port,
    ))
    collection = chroma_client.get_or_create_collection(name=collection_name)
    return collection

def create_chroma_db_local(persist_directory, collection_name):
    chroma_client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=persist_directory,
    ))
    collection = chroma_client.get_or_create_collection(name=collection_name)
    return collection

def insert_to_db(texts, model_name, cuda_idx, db):
    model = sentence_transformers.SentenceTransformer(model_name, device=f"cuda:{cuda_idx}")

    batch_embeddings = []
    batch_texts = []
    start_time = time.time()
    print(f"Total Articles to process: {len(texts)}, Current Thread: {cuda_idx}.")
    for i, text in enumerate(texts):
        # 2. generate embedding
        embeddings = sentence_embedding(model, text).tolist()

        batch_embeddings.append(embeddings)
        batch_texts.append(text)
        # 3. add to vectorstore per 500 articles or last article
        if i % 100 == 0 or i == len(texts)-1:
            batch_ids = [str(uuid.uuid1()) for _ in batch_texts]
            db.add(
                embeddings=batch_embeddings,
                documents=batch_texts,
                ids = batch_ids
            )
            batch_embeddings = []
            batch_texts = []
            print(f"Completed Processing article count: {i}, Current Thread: {cuda_idx}, Time took: {time.time() - start_time}.")
    print(f"Thread {cuda_idx} Completed. Total time took for thread: {time.time() - start_time}.")


# Multi-processing
def query_llm(cuda_idxes, query, is_local=True, start=None, end=None):
    number_of_processes = len(cuda_idxes)
    input_texts = []
    db = create_chroma_db_local(CHROMA_PERSIST_DIRECTORY, CHROMA_COLLECTION_NAME)
    with open(FILE_PATH, 'r') as f:
        for item in jsonlines.Reader(f):
            input_texts.append(item["content"])
    print("Total Number of papers:", len(input_texts))
    # input_texts = np.array_split(input_texts, number_of_processes)

    args = ((input_texts[i], EMBED_MODEL_NAME, cuda_idxes[i], is_local) for i in range(number_of_processes))

    # if there is no file under the directory "/localscratch/yzhuang43/ra-llm/retrieval_benchmark/data/chroma_db/agenda", insert the data into the db
    if len(os.listdir(CHROMA_PERSIST_DIRECTORY)) == 0:
        insert_to_db(input_texts, model_name=EMBED_MODEL_NAME, cuda_idx=0, db=db)

    input_paths = np.array_split(input_texts, number_of_processes)
    with ProcessPoolExecutor(number_of_processes) as executor:
        executor.map(insert_to_db, args)
    model = sentence_transformers.SentenceTransformer(EMBED_MODEL_NAME, device=f"cuda:0")
    query_embedding = sentence_embedding(model, query).tolist()
    results = db.query(query_embeddings=query_embedding, n_results=3)
    retrieval_content = [result for result in results['documents'][0]]
    # print(retrieval_content)
    retrieval_content = '\n'.join(retrieval_content)
    return retrieval_content

def main(cuda_idxes, query):
    print(query_llm(cuda_idxes, query))


if __name__ == '__main__':
    query = "What is the corresponding EM score of the BiDAF__ensemble_ method on SQuAD1_1 dataset for Question_Answering task?"
    db = main([0], query)
    # print("finished running")
    # embedding_model = sentence_transformers.SentenceTransformer(EMBED_MODEL_NAME, device=0)

