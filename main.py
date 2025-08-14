# main.py
import json
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from bson.json_util import dumps
from typing import List

# Importações locais
from db import profissionais_collection, clientes_collection, agendamentos_collection
from schemas import (
    ProfissionalCreate, ClienteCreate, AgendamentoCreate,
    RelatorioTopProfissionais, RelatorioServicosPopulares
)

app = FastAPI(
    title="API de Agenda para Clínica de Estética",
    description="API para gerenciar profissionais, clientes e agendamentos de uma clínica de estética.",
    version="1.0.0"
)

# --- Endpoints de Cadastro --- 

@app.post("/profissionais", summary="Cadastra um novo profissional", tags=["Cadastros"])
def criar_profissional(profissional: ProfissionalCreate):
    result = profissionais_collection.insert_one(profissional.dict())
    return {"id_inserido": str(result.inserted_id), "mensagem": "Profissional cadastrado com sucesso!"}

@app.post("/clientes", summary="Cadastra um novo cliente", tags=["Cadastros"])
def criar_cliente(cliente: ClienteCreate):
    if clientes_collection.find_one({"cpf": cliente.cpf}):
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    clientes_collection.insert_one(cliente.dict())
    return {"mensagem": "Cliente cadastrado com sucesso"}

@app.post("/agendamentos", summary="Cria um novo agendamento", tags=["Cadastros"])
def criar_agendamento(agendamento: AgendamentoCreate):
    if not clientes_collection.find_one({"cpf": agendamento.cpf_cliente}):
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    try:
        if not profissionais_collection.find_one({"_id": ObjectId(agendamento.id_profissional)}):
            raise HTTPException(status_code=404, detail="Profissional não encontrado")
    except Exception:
        raise HTTPException(status_code=400, detail="ID do profissional inválido")
        
    agendamentos_collection.insert_one(agendamento.dict())
    return {"mensagem": "Agendamento realizado com sucesso"}

# --- Endpoint de Busca com Índice ---

@app.get("/profissionais/busca", summary="Busca profissionais pelo nome", response_model=List[dict], tags=["Buscas"])
def buscar_profissional_por_nome(nome: str = Query(..., min_length=2, description="Parte do nome do profissional para buscar")):
    profissionais = list(profissionais_collection.find({"nome": {"$regex": nome, "$options": "i"}}))
    if not profissionais:
        raise HTTPException(status_code=404, detail="Nenhum profissional encontrado com esse nome.")
    
    for p in profissionais:
        p["_id"] = str(p["_id"])
    return profissionais

# --- Endpoints de Relatórios com Aggregation Pipeline ---

@app.get("/relatorios/profissionais-top", summary="Ranking de profissionais com mais agendamentos", response_model=List[RelatorioTopProfissionais], tags=["Relatórios"])
def get_top_profissionais():
    pipeline = [
        {"$group": {"_id": "$id_profissional", "total_agendamentos": {"$sum": 1}}},
        {"$sort": {"total_agendamentos": -1}},
        {"$lookup": {
            "from": "profissionais",
            "localField": "_id",
            "foreignField": "_id_str",
            "as": "profissional_info"
        }},
        {"$unwind": "$profissional_info"},
        {"$project": {
            "_id": 0,
            "nome_profissional": "$profissional_info.nome",
            "especialidade": "$profissional_info.especialidade",
            "total_agendamentos": 1
        }}
    ]
    # Pré-processamento para compatibilidade de tipos no $lookup
    profissionais_collection.update_many({}, [{"$set": {"_id_str": {"$toString": "$_id"}}}])
    
    resultado = list(agendamentos_collection.aggregate(pipeline))
    if not resultado:
        return []
    return JSONResponse(content=json.loads(dumps(resultado)))

@app.get("/relatorios/servicos-populares", summary="Contagem de agendamentos por tipo de serviço", response_model=List[RelatorioServicosPopulares], tags=["Relatórios"])
def get_servicos_populares():
    pipeline = [
        {"$group": {"_id": "$servico", "quantidade": {"$sum": 1}}},
        {"$sort": {"quantidade": -1}},
        {"$project": {
            "_id": 0,
            "servico": "$_id",
            "total_agendamentos": "$quantidade"
        }}
    ]
    resultado = list(agendamentos_collection.aggregate(pipeline))
    if not resultado:
        return []
    return JSONResponse(content=json.loads(dumps(resultado)))