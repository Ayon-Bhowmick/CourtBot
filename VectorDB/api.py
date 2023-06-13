from fastapi import FastAPI, Response, Query, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from chromadb.utils import embedding_functions

api = FastAPI()
# set cors
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# connect db
ef = embedding_functions.InstructorEmbeddingFunction(model_name="hkunlp/instructor-large", device="cuda")
client = chromadb.Client()
collection = client.get_or_create_collection(name="cases", embedding_function=ef, metadata={"hnsw:space": "cosine"})

@api.get("/query")
async def query(question: str = Body(..., embed=True), num_res: int = Body(..., embed=True)):
    """
    gets nearby embedings from question
    :params: question: question to query
    :params: num_res: number of responces to return
    :return: n nearest neighbors to the question
    """
    res = collection.query(query_texts=[question], n_results=num_res)
    return res
