import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os

if __name__ == "__main__":
    # make collection
    ef = embedding_functions.InstructorEmbeddingFunction(model_name="hkunlp/instructor-large", device="cuda")
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="cases", embedding_function=ef, metadata={"hnsw:space": "cosine"})

    # add documents
    for case in os.listdir("../SupremeCourtCases"):
        with open("../SupremeCourtCases/" + case, "r") as f:
            case_name = case[:-4]
            text = f.read().split("\n")
            lines = len(text)
            metadata = [{"case": case_name, "paragraph": i} for i in range(lines)]
            ids = [f"{case_name}_{i}" for i in range(lines)]
        collection.add(documents=text, ids=ids, metadatas=metadata)
        print(f"Added {case_name} to collection")

    # test
    print()
    print(collection.query(query_texts=["Alcohol"], n_results=10))
    print(collection.query(query_texts=["Segregation"], n_results=10))
