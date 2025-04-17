from pymongo import MongoClient
from CTkMessagebox import CTkMessagebox

def connect():
    try:
        uri = ""
        db = MongoClient(uri)
        return db["security_pay"]
    except Exception as e:
        print("erro " + str(e))
        return CTkMessagebox(title="Erro", icon="warning", message=f"Ocorreu um erro: {str(e)}")  
