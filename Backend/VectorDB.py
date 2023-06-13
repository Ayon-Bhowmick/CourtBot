import chromadb
from chromadb.utils import embedding_functions
import os

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
    for case in os.listdir("../SupremeCourtCases"):
        with open("../SupremeCourtCases/" + case, "r") as f:
            case_name = case[:-4]
            text = f.read().split("\n")
            num_lines = len(text)
            metadata = [{"case": case_name, "paragraph": i} for i in range(num_lines)]
            ids = [f"{case_name}_{i}" for i in range(num_lines)]
        collection.add(documents=text, ids=ids, metadatas=metadata)
        print(f"Added {case_name} to collection")

    # test
    print()
    print(collection.query(query_texts=["Alcohol"], n_results=10))
    print(collection.query(query_texts=["Segregation"], n_results=10))
