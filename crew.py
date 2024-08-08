from agents import ChatAgent, Agent
from config import *
from memory import ConversationalMemory
from duckduckgo_search import DDGS

if __name__ == '__main__':
    llm = 'llama3.1:latest'
    duckduckgo = DDGS()
    
    researcher_tools_map = {
        'DDGS_text': duckduckgo.text,
        'DDGS_news': duckduckgo.news,
    }
    ddgs_news_tool = {
        'type': 'function',
        'function': {
          'name': 'DDGS_news',
          'description': 'Get Duck Duck Go to fetch latest news results from INTERNET about the keywords.',
          'parameters': {
            'type': 'object',
            'properties': {
              'keywords': {
                'type': 'string',
                'description': 'keywords to search over Internet.',
              },
              'max_results': {
                'type': 'int',
                'description': 'number of results required from the search',
              },
            },
            'required': ['keywords', 'max_results'],
          },
        },
      }

    ddgs_text_tool = {
        'type': 'function',
        'function': {
          'name': 'DDGS_text',
          'description': 'Get Duck Duck Go to search results from INTERNET about the keywords.',
          'parameters': {
            'type': 'object',
            'properties': {
              'keywords': {
                'type': 'string',
                'description': 'keywords to search over Internet.',
              },
              'max_results': {
                'type': 'int',
                'description': 'number of results required from the search',
              },
            },
            'required': ['keywords', 'max_results'],
          },
        },
      }
    
    researcher_tools = [ddgs_text_tool, ddgs_news_tool]
    # researcher_memory_collection = memory_db_client.get_or_create_collection('researcher_memory')
    # researcher_memory = ConversationalMemory(researcher_memory_collection)
    researcher = ChatAgent(
        model = llm,
        name = 'researcher',
        role = 'You are a expert Reseacher. Given access to Internet you can use provied tools to search about the given Query.',
        tools = researcher_tools
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
