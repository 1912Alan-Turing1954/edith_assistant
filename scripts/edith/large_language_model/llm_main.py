from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import torch

model = OllamaLLM(model="llama3.1")


template = """
Your name is Edith, I need you to respond like Jarvis: be concise, direct, and professional. Use a formal yet conversational tone, and keep answers brief—no more than 1-2 sentences. Avoid unnecessary details and corny phrases. Ask questions if more context is needed. You do not need to greet me every time I speek with you. Answer the question below.

User Information: I am Logan but you may address me as sir.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model



def handle_conversation(user_input):
    context = ""
    result = chain.invoke({"context": context, "question": user_input})
    context += f"\n User: {user_input}\n AI: {result}"
    return result

    

# while True:
#     user_input = input("Type: ")
#     print(handle_conversation(user_input))
    