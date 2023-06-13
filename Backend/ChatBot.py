from transformers import pipeline

class Conversation:
    def __init__(self):
        self.MODEL_NAME = "deepset/tinyroberta-squad2" # https://huggingface.co/deepset/tinyroberta-squad2
        self.BOT = pipeline('question-answering', model=self.MODEL_NAME, tokenizer=self.MODEL_NAME)
        self.conversation: list[dir[str, str]] = []

    def get_conversation(self) -> str:
        """
        gets the duration of the conversation in a format which can be passed as context
        :return: conversation as a str
        """
        
    
    def ask(self, question: str, context: str):
        """
        gets the bot's responce given a question and context
        :params: question: user inputed prompt
        :params: context: context from database
        :return: responce from bot
        """
        input = {"question": question, "context": context}
        res = self.BOT(input)
        return res
