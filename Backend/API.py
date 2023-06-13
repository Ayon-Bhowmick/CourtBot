from fastapi import FastAPI, Response, Query, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import VectorDB
from ChatBot import Conversation

api = FastAPI()
# set cors
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
convo = Conversation()

@api.get("/query")
async def query(question: str = Body(..., embed=True), num_res: int = Body(..., embed=True)):
    """
    gets nearby embedings from question
    :params: question: question to query
    :params: num_res: number of responces to return
    :return: n nearest neighbors to the question
    """
    return VectorDB.query(question, num_res)

@api.put("/reset")
async def reset():
    """
    reset conversation
    """
    convo = Conversation()

@api.get("/ask")
async def ask(question: str = Body(..., embed=True)):
    """
    askes chat bot a question with context
    :params: question: user inputer question
    :return: chat bot's responce
    """
    context = VectorDB.query(question, 10)
    res = convo.ask(question, context)
    return res
