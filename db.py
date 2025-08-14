# db.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi  # Importe a biblioteca certifi

load_dotenv()

db_user = os.getenv("DBUSER")
db_secret = os.getenv("DBSECRET")

cluster_address = "cluster0.7wgscfr.mongodb.net"
mongo_uri = f"mongodb+srv://{db_user}:{db_secret}@{cluster_address}/?retryWrites=true&w=majority&appName=Cluster0"

# Adicione o parâmetro tlsCAFile ao criar o cliente
client = MongoClient(mongo_uri, tlsCAFile=certifi.where())

db = client["clinica_estetica"]

profissionais_collection = db["profissionais"]
clientes_collection = db["clientes"]
agendamentos_collection = db["agendamentos"]

print("Verificando e criando índice para 'profissionais'...")
profissionais_collection.create_index([("nome", 1)], name="idx_nome_profissional")
print("Índice pronto.")