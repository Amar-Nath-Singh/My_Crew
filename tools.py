from chromadb import Collection

def generate_pdf_embedding(pdf_path, pdf_collection_name):
    pass

def pdf_query(collection, query_embeddings):
    pass


class ToolNode:
    def __init__(self, type_ : str, name : str, description : str, parameters : dict, required_params : list, response) -> None:
        self.details = {
                'type': type_,
                type_: {
                'name': name,
                'description': description,
                'parameters': parameters,
                    'required': required_params,
                },
            }

        self.repsonse = response
        
        