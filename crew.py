from agents import ChatAgent, Agent


if __name__ == '__main__':
    llm = 'llama3.1:latest'
    ceo = ChatAgent(
        model=llm, 
        name='CEO', 
        role='You are the CEO of Google. You make sure that your company runs smoothly and you empower your employees to innovate and lead in technology. Your responsibilities include overseeing company operations, making strategic decisions, and representing Google at public and private events. You prioritize maintaining a positive company culture and ensuring the well-being of your team.'
    )
