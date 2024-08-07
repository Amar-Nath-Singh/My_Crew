from memory import ConversationalMemoryClustering
from config import *
from utils import *

class ChatAgents:
    def __init__(self, model, name, role) -> None:
        self.model = model
        self.role = role
        self.name = name
        self.collection = memory_db_client.get_or_create_collection(f'{self.name}_mem')
        self.memory = ConversationalMemoryClustering(collection=self.collection)

        self.system_message = [{
            'role':'system',
            'content': self.role,
        }]

    def response(self, message):
        mem = self.memory.retrive_memory(message)
        self.memory.ingest_conversation(message)

        messages = self.system_message + mem + [message]
        msgs = "\n".join(list(map(str, messages)))
        print(f'{bcolors.OKBLUE} {msgs} {bcolors.ENDC}')

        resp_message = llm_client.chat(self.model, messages=messages, options = {"temperature": 0 })['message']
        self.memory.ingest_conversation(resp_message)

        return resp_message



if __name__ == '__main__':
    agent = ChatAgents('llama3.1:8b-instruct-fp16', 'Writer', 'You are a excellent poem writer. You can only converse in poetic manner.')

    while True:
        inp_role = 'user'
        inp_content = input('content :')
        if inp_content == '/bye':
            break
        message = {
            'role' : inp_role,
            'content' : inp_content,
        }
        print(f'{bcolors.OKGREEN} {agent.response(message)} {bcolors.ENDC}')