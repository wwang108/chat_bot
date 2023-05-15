import time
from typing import List, Tuple
from langchain import OpenAI
import os
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import RetrievalQA
from langchain.llms import OpenAIChat
from langchain.vectorstores import DeepLake

class CampingChatbot:
    def __init__(self, dataset_path: str, embeddings: OpenAIEmbeddings, token_limit: int = 4096, timeout: int = 300):
        db = DeepLake(dataset_path=dataset_path, embedding_function=embeddings, read_only=True)
        self.qa =  ConversationalRetrievalChain.from_llm(
            OpenAI(temperature=0),
            retriever=db.as_retriever()
        )
        self.chat_history: List[Tuple[str, str]] = []
        self.token_limit = token_limit
        self.timeout = timeout
        self.last_interaction = time.time()

    def receive_message(self, message: str) -> str:
        if time.time() - self.last_interaction > self.timeout:
            self.reset_chat_history()

        result = self.qa({"question": message, "chat_history": self.chat_history})

        while self.calculate_token_count(self.chat_history) + len(message) + len(result["answer"]) > self.token_limit:
            self.chat_history.pop(0)

        self.chat_history.append((message, result["answer"]))
        self.last_interaction = time.time()
        return result["answer"]

    def reset_chat_history(self):
        self.chat_history = []

    @staticmethod
    def calculate_token_count(chat_history: List[Tuple[str, str]]) -> int:
        return sum(len(question) + len(answer) for question, answer in chat_history)

# 示例用法：
# os.environ['OPENAI_API_KEY'] =
# persist_directory = 'db'
# embedding = OpenAIEmbeddings()
# vectordb = Chroma(persist_directory=persist_directory,
#                   embedding_function=embedding)
# vectorstore = vectordb  # 使用前面的方法创建一个Chroma对象
# chatbot = CampingChatbot(vectorstore)

# response = chatbot.receive_message("What is camping?")
# print(response)

# response = chatbot.receive_message("How to get a good camping experience?")
# print(response)
