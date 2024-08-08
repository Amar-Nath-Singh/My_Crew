from config import *
from utils import *
from copy import deepcopy
from prompts import *

class ChatAgent:
    def __init__(self, model, name, role, memory = None, tools = None
                 ) -> None:
        self.model = model
        self.role = role

        self.name = name
        self.memory = memory
        self.tools = tools

        system_prompt = self.role + \
            ('\n' + TOOLUSAGE + '\n'.join([f'name: {tool.name}\nrole: {tool.role}' for tool in tools])) \
                if self.tools else ''
        
        self.system_message = [{
            'role':'system',
            'content': system_prompt,
        }]



    def response(self, message, stream = False):
        messages = deepcopy(self.system_message)
        if self.memory:
            mem = self.memory.retrive_memory(message)
            messages.extend(mem)
            msgs = "\n".join(list(map(str, messages)))
            print(f'{bcolors.OKBLUE} {msgs} {bcolors.ENDC}')
        
        print(f'{self.name}: {bcolors.OKCYAN} {message} {bcolors.ENDC}')
        messages.append(message)
        
        response = llm_client.chat(self.model, 
                                   messages = messages, 
                                   tools = self.tools,
                                   stream = stream,
                                   options = {"temperature": 0 })

        if self.memory:
            resp_message = response['message']
            self.memory.ingest_conversation(resp_message)
            self.memory.ingest_conversation(message)

        return response

    async def response_async(self, message, stream = False):
        messages = self.system_message.copy()
        if self.memory:
            mem = self.memory.retrive_memory(message)
            messages.extend(mem)
            msgs = "\n".join(list(map(str, messages)))
            print(f'{bcolors.OKBLUE} {msgs} {bcolors.ENDC}')
        print(f'{self.name}: {bcolors.OKCYAN} {message} {bcolors.ENDC}')
        messages.append(message)

        response = await llm_client_async.chat(self.model, 
                                   messages=messages, 
                                   tools = self.tools,
                                   stream=stream,
                                   options = {"temperature": 0 })

        if self.memory:
            resp_message = response['message']
            self.memory.ingest_conversation(resp_message)
            self.memory.ingest_conversation(message)

        return response

class Agent:
    def __init__(self, model, name, role, format = '') -> None:
        self.model = model
        self.role = role
        self.name = name
        self.format = format
        self.system_message = [{
            'role':'system',
            'content': self.role,
        }]

        self.context = None

    def response(self, message, keep_context = False):
        print(f'{self.name}: {bcolors.OKCYAN} {message} {bcolors.ENDC}')

        resp_message = llm_client.generate(
            model = self.model,
            prompt = message,
            system = self.role,
            format = self.format,
            context = self.context,
            options = {"temperature": 0 })

        if keep_context:
            self.context = resp_message['context']
        else:
            self.context = None
        
        return resp_message['response']
    
    async def response_async(self, message, keep_context = False, stream = False):
        print(f'{self.name}: {bcolors.OKCYAN} {message} {bcolors.ENDC}')

        resp_message = await llm_client_async.generate(
            model = self.model,
            prompt = message,
            system = self.role,
            format = self.format,
            context = self.context,
            stream = stream,
            options = {"temperature": 0 })

        if keep_context:
            self.context = resp_message['context']
        else:
            self.context = None
        
        return resp_message['response']

if __name__ == '__main__':
    agent = Agent(model = 'llama3.1:latest', name = 'Writer', role = 'You are a excellent poem writer. You can only converse in poetic manner.')

    while True:
        inp_content = input('content :')
        if inp_content == '/bye':
            break
        print(f'{bcolors.OKGREEN} {agent.response(inp_content)} {bcolors.ENDC}')
