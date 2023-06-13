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
        ret = ""
        for chat in self.conversation:
            ret += f" user: {chat['user']} "
            ret += f" CourtBot: {chat['bot']} "
        return ret
    
    def ask(self, question: str, context: str):
        """
        gets the bot's responce given a question and context
        :params: question: user inputed prompt
        :params: context: context from database
        :return: responce from bot
        """
        full_context = f"Conversation so far: {self.get_conversation()} referance material:{context}"
        input = {"question": question, "context": full_context}
        res = self.BOT(input)
        self.conversation.append({"user": question, "CourtBot": res})
        return res
