# popular.py
from pymongo import MongoClient
from datetime import datetime, timedelta
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

print("Limpando coleções existentes...")
profissionais_collection.delete_many({})
clientes_collection.delete_many({})
agendamentos_collection.delete_many({})

print("Inserindo profissionais...")
profissionais = [
    {"nome": "Ana Paula", "especialidade": "Esteticista Facial"},
    {"nome": "Bruno Lima", "especialidade": "Massoterapeuta"},
    {"nome": "Carla Mendes", "especialidade": "Manicure e Pedicure"}
]
result_profissionais = profissionais_collection.insert_many(profissionais)
profissionais_ids = result_profissionais.inserted_ids

# ... (o resto do arquivo continua igual) ...

print("Inserindo clientes...")
clientes = [
    {"nome": "Mariana Costa", "cpf": "11122233344", "telefone": "34991112222"},
    {"nome": "Fernanda Souza", "cpf": "55566677788", "telefone": "34992223333"},
    {"nome": "Ricardo Almeida", "cpf": "99988877766", "telefone": "34993334444"}
]
clientes_collection.insert_many(clientes)

print("Inserindo agendamentos de exemplo...")
agendamentos = [
    {"cpf_cliente": "11122233344", "id_profissional": str(profissionais_ids[0]), "servico": "Limpeza de Pele", "data_hora": datetime.now() + timedelta(days=5)},
    {"cpf_cliente": "99988877766", "id_profissional": str(profissionais_ids[0]), "servico": "Peeling de Diamante", "data_hora": datetime.now() + timedelta(days=8)},
    {"cpf_cliente": "11122233344", "id_profissional": str(profissionais_ids[0]), "servico": "Drenagem Linfática Facial", "data_hora": datetime.now() + timedelta(days=15)},
    {"cpf_cliente": "99988877766", "id_profissional": str(profissionais_ids[1]), "servico": "Massagem Relaxante", "data_hora": datetime.now() + timedelta(days=7)},
    {"cpf_cliente": "55566677788", "id_profissional": str(profissionais_ids[2]), "servico": "Manicure e Pedicure", "data_hora": datetime.now() + timedelta(days=3)},
    {"cpf_cliente": "11122233344", "id_profissional": str(profissionais_ids[2]), "servico": "Manicure", "data_hora": datetime.now() + timedelta(days=12)},
]
agendamentos_collection.insert_many(agendamentos)
print("Banco de dados populado com sucesso!")