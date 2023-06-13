import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import InstructorEmbedding
import os

if __name__ == "__main__":
    # make collection
    ef = embedding_functions.InstructorEmbeddingFunction(model_name="hkunlp/instructor-large", device="cuda")
    client = chromadb.Client()
    collection = client.get_or_create_collection (Settings(anonymized_telemetry=False), name="cases", embedding_function=ef, metadata={"hnsw:space": "cosine"})

    # add documents
    for case in os.listdir("../SupremeCourtCases"):
        with open("../SupremeCourtCases/" + case, "r") as f:
            text = f.read().split("\n")
            metadata = [{"case": case.split(".")[0], "paragraph": i} for i in range(len(text))]
            
