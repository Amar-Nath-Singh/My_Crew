from ollama import Client, AsyncClient
import chromadb

# llm_client = Client(host='http://10.21.139.236:11434')
llm_client = Client(host='http://127.0.0.1:11434')
llm_client_async = AsyncClient(host='http://127.0.0.1:11434')
memory_db_client = chromadb.PersistentClient("./memory_db")
embedding_model = 'nomic-embed-text:latest'

if __name__ == '__main__':
    print(llm_client.list())
