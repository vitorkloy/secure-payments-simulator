from pymongo import MongoClient
from CTkMessagebox import CTkMessagebox
from dotenv import load_dotenv
import os

load_dotenv()  

def connect():
    try:
        uri = os.getenv("MONGODB_URI") 
        db = MongoClient(uri)
        return db["security_pay"]
    except Exception as e:
        print("erro " + str(e))
        return CTkMessagebox(title="Erro", icon="warning", message=f"Ocorreu um erro: {str(e)}")