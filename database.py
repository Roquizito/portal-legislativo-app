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
    """Busca os projetos em cache por 60 segundos para otimizar a performance."""
    response = _supabase.table("dim_projetos").select("SK_projeto, numero_ano_projeto").execute()
    return response.data

@st.cache_data(ttl=3600)
def fetch_setores(_supabase: Client) -> list:
    """Busca os setores disponíveis. Cache longo pois setores mudam raramente."""
    response = _supabase.table("dim_setores").select("SK_setor, nome_setor").execute()
    return response.data

def insert_projeto(supabase: Client, data: dict) -> None:
    """Valida e insere um novo projeto na dimensão."""
    if not data.get("numero_ano_projeto") or not data.get("protocolo"):
        raise ValueError("Os campos 'Número/Ano' e 'Protocolo' são estritamente obrigatórios.")
    supabase.table("dim_projetos").insert(data).execute()
    # Limpa o cache após a inserção para refletir os novos dados imediatamente
    fetch_projetos.clear()

def insert_autor(supabase: Client, data: dict) -> None:
    """Valida e insere um novo autor na dimensão."""
    if not data.get("nome_autor"):
        raise ValueError("O 'Nome Completo do Autor' é obrigatório.")
    supabase.table("dim_autores").insert(data).execute()

def insert_tramitacao(supabase: Client, data: dict) -> None:
    """Valida as chaves e insere o evento de tramitação na tabela fato."""
    if data.get("SK_setor_origem") == data.get("SK_setor_destino"):
        raise ValueError("O setor de origem não pode ser idêntico ao de destino.")
    supabase.table("fato_tramitacoes").insert(data).execute()