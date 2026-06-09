# database.py
from supabase import create_client, Client
import streamlit as st

@st.cache_resource
def get_connection() -> Client:
    """Inicializa e mantém a conexão com o Supabase de forma otimizada."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

@st.cache_data(ttl=60)
def fetch_projetos(_supabase: Client) -> list:
    """Busca a lista central de projetos para popular os menus dropdown."""
    response = _supabase.table("projeto_lei").select("id, numero_projeto, autor_nome").execute()
    return response.data

def insert_projeto_central(supabase: Client, data: dict) -> None:
    """Insere os dados fundamentais do projeto e do autor na super tabela."""
    supabase.table("projeto_lei").insert(data).execute()
    fetch_projetos.clear()  # Invalida o cache para atualizar a interface em tempo real

def update_projeto_localizacao(supabase: Client, id_projeto: int, data: dict) -> None:
    """Atualiza colunas mutáveis (setor, relator, status) de um projeto existente."""
    supabase.table("projeto_lei").update(data).eq("id", id_projeto).execute()
    fetch_projetos.clear()

def insert_parecer(supabase: Client, data: dict) -> None:
    """Insere um registo na tabela satélite (Relação 1:N), preservando o histórico."""
    supabase.table("parecer").insert(data).execute()