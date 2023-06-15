import chromadb
from chromadb.utils import embedding_functions
import os

MIN_LENGTH = 16
# make collection
ef = embedding_functions.InstructorEmbeddingFunction(model_name="hkunlp/instructor-large", device="cuda")
client = chromadb.Client()
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
    collection.add(documents=docs, ids=ids, metadatas=metadata)

if __name__ == "__main__":
    # add documents
    for i, case in enumerate(os.listdir("../SupremeCourtCases")):
        with open("../SupremeCourtCases/" + case, "r") as f:
            case_name = case[:-4]
            text = [line for line in f.read().split("\n") if len(line) >= MIN_LENGTH]
            num_lines = len(text)
            metadata = [{"case": case_name, "paragraph": j} for j in range(num_lines)]
            ids = [f"{i}_{j}" for j in range(num_lines)]
        collection.add(documents=text, ids=ids, metadatas=metadata)
        print(f"Added {case_name} to collection")
    collection

    # test
    print()
    print(collection.query(query_texts=["Segregation"], n_results=10))
    print(collection.query(query_texts=["Alcohol"], n_results=10))
    print(collection.query(query_texts=["Tell me about the supreme court's opinions on segregation"], n_results=10))
