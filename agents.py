from config import *
from utils import *
from copy import deepcopy
from prompts import *

class Agent:
    def __init__(self, model, name, agent_desp, agent_use, agent_requires = '', tools = [], properties = {}, required = []) -> None:
        self.model = model
        self.name = name
        self.agent_desp = agent_desp
        self.tools_exec_map = {
            tool.name: tool for tool in tools
        }
        self.tools = [tool.details for tool in tools]

        properties['query'] = {
                    "type": "string",
                    "description": agent_requires,
                }
        required.append('query')
        self.details = {
            "name": name,
            "description": agent_desp,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    
    def bind_tool(self, tool):
        if not tool.name in self.tools_exec_map:
            self.tools_exec_map[tool.name] = tool
            self.tools.append(tool.details)

    def response(self, query, context = None):
        print(f'{self.name}: {bcolors.OKCYAN} {query} {bcolors.ENDC}')
        response = None
        if len(self.tools):
            prompt = AGENT_THOUGHT_PROMPT(self.agent_desp, self.tools, query=query)
            thought_gen = llm_client.generate(
                model = self.model,
                prompt = prompt,
                format = 'json',
                context = None,
                options = {"temperature": 0})
            
            thought_resp: dict = json.loads(thought_gen['response'])
            thought = thought_resp.get('Thought', None)
            actions = thought_resp.get('Actions', [])

            observations = []

            print(f'{self.name} THOUGHT: {bcolors.OKCYAN} {thought} {bcolors.ENDC}')
            context = None
            for action_df in actions:
                action_df: dict
                action = action_df.get('Action', None)
                tool_calls = action_df.get('tool_calls', [])

                print(f'{self.name}: {bcolors.OKBLUE} {action} {tool_calls} {bcolors.ENDC}')
                for tool_df in tool_calls:
                    tool_df: dict
                    tool_name = tool_df.get('name', None)
                    tool_args = tool_df.get('parameters', None)
                    tool_args['context'] = context

                    if tool_name and tool_name in self.tools_exec_map:
                        tool_exec_resp = self.tools_exec_map[tool_name].response(**tool_args)
                        if tool_exec_resp:
                            context = tool_exec_resp['context']
                            observations.append((action, tool_exec_resp['response']))
        
            if len(observations):

                obs_str = '\n'.join(f'Action: {obs[0]} Observation: {obs[1]}' for obs in observations)
                response_prompt = AGENT_RESPONSE_PROMPT(agent_desp=self.agent_desp, 
                                                        thought=thought,
                                                        observations=obs_str,
                                                        query=query)

            else:
                response_prompt = AGENT_RESPONSE_NO_OBSERVATIONS_PROMPT(agent_desp=self.agent_desp, 
                                                        thought=thought,
                                                        query=query)
            response = llm_client.generate(
                        model = self.model,
                        prompt = response_prompt,
                        format = '',
                        options = {"temperature": 0 })

        if not response:
            response = llm_client.generate(
                                model = self.model,
                                prompt = query,
                                system = self.agent_desp,
                                format = '',
                                options = {"temperature": 0 })
        
        print(f'{self.name} RESPONSE: {bcolors.OKGREEN} {response["response"]} {bcolors.ENDC}')
        return response
        
if __name__ == '__main__':
    poet = Agent(model = 'llama3.1:latest', name = 'poet', 
                  agent_desp = 'You are a excellent poem writer. You can only converse in poetic manner.',
                  agent_use = 'Use to convert any text into poetic tone.',
                  agent_requires = 'Any kind of text that needs to converted into poetic tone.')
    
    hinglish_writer = Agent(model='llama3.1:latest', 
                name='hinglish_Writer', 
                agent_desp = 'You are a Hinglish Writer. You takes any text and rewrites it into Hinglish which is Hindi written in English.', 
                agent_use = 'Use to convert any English text to Hinglish.',
                agent_requires='Any text that needs to be transformed into Hinglish language or any conversation to be held in a Hinglish style.')
    
    manager = Agent(model = 'llama3.1:latest', name = 'manager', 
                  agent_desp = 'You are the Manager of a Newspaper Company. You take topics to publish on newpaper and reports back with completed article for review.',
                  agent_use = 'Use to generate content on topics. This can assign work to other employees like poet and hinglish_writer',
                  agent_requires = 'Topic on to be published in Newpaper, or any correction to be done in publication or Topic.',
                  tools = [poet, hinglish_writer])

    boss = Agent(model = 'llama3.1:latest', name = 'boss', 
                  agent_desp = 'You are the Boss of a Newspaper Company. You analyse work of you employees suggest required changes.',
                  agent_requires = 'Topic with content to be reviwed before publishing.',
                  tools = [manager])

    manager.bind_tool(boss)

    while True:
        inp_content = input('content :')
        if inp_content == '/bye':
            break
        boss.response(inp_content)
