import pymongo

class ConexaoMongoDB:
    def __init__(self):
        # Conectar ao servidor do MongoDB (neste exemplo, está sendo utilizado o MongoDB local)
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        # Selecionar o banco de dados (ou criar um novo se não existir)
        self.db = self.client["meu_banco_de_dados"]
        # Selecionar a coleção (ou criar uma nova se não existir)
        self.colecao = self.db["minha_colecao"]

    def inserir_registro(self, registro):
        # Inserir o registro na coleção
        resultado = self.colecao.insert_one(registro)
        # Retornar o ID do documento inserido
        return resultado.inserted_id
