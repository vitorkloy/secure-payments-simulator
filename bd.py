from pymongo import MongoClient
from CTkMessagebox import CTkMessagebox

def connect():
    try:
        uri = "mongodb+srv://root:Bb4iuGBz46mB3Ioq@mongodb.hfi0yre.mongodb.net/?retryWrites=true&w=majority&appName=mongoDB"
        db = MongoClient(uri)
        return db["security_pay"]
    except Exception as e:
        print("erro " + str(e))
        return CTkMessagebox(title="Erro", icon="warning", message=f"Ocorreu um erro: {str(e)}")  
