# database.py
from supabase import create_client, Client
import streamlit as st

@st.cache_resource
def get_connection() -> Client:
    """Inicializa e mantém a conexão com o Supabase em cache."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

@st.cache_data(ttl=60)
def fetch_projetos(_supabase: Client) -> list:
    """Busca os projetos na tabela física 'projeto_lei'."""
    response = _supabase.table("projeto_lei").select("*").execute()
    return response.data

def insert_projeto(supabase: Client, data: dict) -> None:
    """Insere um novo projeto na tabela 'projeto_lei'."""
    supabase.table("projeto_lei").insert(data).execute()
    fetch_projetos.clear()

def insert_autor(supabase: Client, data: dict) -> None:
    """Insere um novo autor na tabela 'autor'."""
    supabase.table("autor").insert(data).execute()

def insert_tramitacao(supabase: Client, data: dict) -> None:
    """Insere o evento de tramitação na tabela 'tramitacao'."""
    supabase.table("tramitacao").insert(data).execute()