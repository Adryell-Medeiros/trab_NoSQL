# schemas.py
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# --- Schemas para Criação ---

class ProfissionalCreate(BaseModel):
    nome: str
    especialidade: str

class ClienteCreate(BaseModel):
    cpf: str = Field(..., description="CPF do cliente, usado como identificador único")
    nome: str
    telefone: str

class AgendamentoCreate(BaseModel):
    cpf_cliente: str
    id_profissional: str
    servico: str
    data_hora: datetime

# --- Schemas para Respostas de Relatórios ---

class RelatorioTopProfissionais(BaseModel):
    nome_profissional: str
    especialidade: str
    total_agendamentos: int

class RelatorioServicosPopulares(BaseModel):
    servico: str
    total_agendamentos: int