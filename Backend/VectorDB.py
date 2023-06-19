import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
import os
import time

# make collection
ef = embedding_functions.InstructorEmbeddingFunction(model_name="sentence-transformers/all-mpnet-base-v2", device="cuda") # https://huggingface.co/sentence-transformers/all-mpnet-base-v2
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chromadb"))
collection = client.get_or_create_collection(name="cases", embedding_function=ef, metadata={"hnsw:space": "cosine"})

def query(question: str, n: int):
    """
    gets nearby embedings from question
    :params: question: question to query
    :params: n: number of responces to return
    :return: n nearest neighbors to the question
    """
    res = collection.query(query_texts=[question], n_results=n)
    return res

def add(docs: list[str], ids: list[str], metadata: list[dict[str, str]]):
    """
    adds docs to vector database
    :params: docs: list of strings to embed and and to db
    :params: ids: ids conisponding to the docs
    :params: metadata: metadata for the docs
    """
    try:
        collection.add(documents=docs, ids=ids, metadatas=metadata)
        return 0
    except Exception as e:
        raise e

if __name__ == "__main__":
    start = time.time()
    # add documents
    for i, case in enumerate(os.listdir("../SupremeCourtCases")):
        with open("../SupremeCourtCases/" + case, "r") as f:
            case_name = case[:-4]
            text = [line for line in f.read().split("\n")]
            num_lines = len(text)
            metadata = [{"case": case_name, "paragraph": j} for j in range(num_lines)]
            ids = [f"{i}_{j}" for j in range(num_lines)]
        try:
            collection.add(documents=text, ids=ids, metadatas=metadata)
            print(f"Added {case_name} to collection")
        except chromadb.errors.IDAlreadyExistsError as IDerror:
            print(f"{case_name} already in collection")
            continue

    seconds = time.time() - start
    minutes = seconds // 60
    seconds = seconds - minutes * 60
    hours = minutes // 60
    minutes = minutes - hours * 60
    print(f"Total time: {int(hours)}:{int(minutes)}:{seconds}")
