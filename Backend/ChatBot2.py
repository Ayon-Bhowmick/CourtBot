from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("microsoft/GODEL-v1_1-large-seq2seq")
model = AutoModelForSeq2SeqLM.from_pretrained("microsoft/GODEL-v1_1-large-seq2seq")

class Conversation:
    def __init__(self):
        self.dialog = []
        self.instructions = "Answer questions regarding supreme court cases based on the given context and knowledge"
        self.device = "cuda"

    def generate(self, knowledge):
        if knowledge != "":
            knowledge = "[KNOWLEDGE] " + knowledge
        chat = " EOS ".join(self.dialog)
        query = f"{self.instructions} [CONTEXT] {chat} {knowledge}"
        input_ids = tokenizer(query, return_tensors="pt").to(self.device).input_ids
        outputs = model.generate(input_ids, max_length=1500, min_length=8, top_p=0.9, do_sample=True).to(self.device)
        output = tokenizer.decode(outputs[0], skip_special_tokens=True).to(self.device)
        return output

    def ask(self, question: str, context: str):
        self.dialog.append(question)
        out = self.generate(str(context))
        return out
