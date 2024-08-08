from agents import ChatAgent, Agent
from config import *
from memory import ConversationalMemory
from duckduckgo_search import DDGS

if __name__ == '__main__':
    llm = 'llama3.1:latest'
    nodes = []
    graph = {}

    researcher = ChatAgent(
        model = llm,
        name = 'researcher',
        role = 'You are a expert Reseacher. Given access to Internet you can use provied tools to search about the given Query.',
        tools = [child for child in graph['graph'] if child] if 'researcher' in graph else None
    )

    while True:
        inp_content = input('content :')
        if inp_content == 'bye':
            break
        message = {
            'role' : 'user',
            'content' : inp_content,
        }
        print(researcher.response(message))
