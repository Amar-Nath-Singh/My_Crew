import json
from chromadb import Collection
from config import *

class ConversationalMemoryClustering:
    def __init__(self, collection : Collection) -> None:
        self.model = embedding_model
        self.collection = collection
        self.start_id = len(self.collection.get()["ids"])

        self.iter = 0
                
    def ingest_conversation(self, message):
        json_data = json.dumps(message)

        self.collection.add(
            ids = [f'{self.collection.name}_{self.start_id + self.iter}'],
            embeddings = [llm_client.embeddings(self.model, json_data)['embedding']],
            documents = [json_data]
        )

        self.iter += 1

    def retrive_memory(self, message, n_results = 10, prev_results = 10):
        json_data = json.dumps(message)
        response = self.collection.query(
            query_embeddings = [llm_client.embeddings(self.model, json_data)['embedding']],

            n_results = n_results
        )
        sim_mem_ids_docs =  sorted(zip(response['ids'][0], response['documents'][0]), reverse = True)
        mem_id = set()
        mem = []

        for iter_ in range(self.iter - 1, max(-1, self.iter - prev_results - 1), -1):
            id_ = f'{self.collection.name}_{self.start_id + iter_}'
            mem_id.add(id_)
            doc = self.collection.get(id_)['documents'][0]
            mem.append(json.loads(doc))

        for sim_mem_id, sim_mem_doc in sim_mem_ids_docs:
            if sim_mem_id in mem_id:
                continue
            mem_id.add(sim_mem_id)
            mem.append(json.loads(sim_mem_doc))

        return mem

if __name__ == '__main__':
    embedding_model = 'nomic-embed-text:latest'
    collection_name = 'test_memory'
    
    collection = memory_db_client.get_or_create_collection(name=collection_name)
    memory = ConversationalMemoryClustering(collection=collection)

    while True:
        inp_role = input('role :')
        inp_content = input('content :')
        if inp_role == 'bye':
            break
        message = {
            'role' : inp_role,
            'content' : inp_content,
        }
        print(memory.retrive_memory(message, 10))
        memory.ingest_conversation(message)
