# app.py
import streamlit as st
from supabase import create_client, Client

# Configuração da Página
st.set_page_config(page_title="Sistema de Inserção Legislativa", layout="wide")
st.title("🏛️ Portal de Gestão Legislativa da Câmara Municipal (Mossoró/RN)")
st.markdown("Interface transacional para inserção no banco de dados estruturado.")


# Inicialização da conexão com o Supabase
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


supabase: Client = init_connection()

# Criação de abas para organizar a interface
tab_projetos, tab_autores, tab_tramitacao = st.tabs([
    "Cadastrar Projeto (Dimensão)",
    "Cadastrar Autor (Dimensão)",
    "Registrar Tramitação (Fato)"
])

# ---------------------------------------------------------
# ABA 1: DIM_PROJETOS
# ---------------------------------------------------------
with tab_projetos:
    st.header("Novo Projeto de Lei")
    with st.form("form_projetos", clear_on_submit=True):
        col1, col2 = st.columns(2)
        numero_ano = col1.text_input("Número/Ano do Projeto", placeholder="Ex: 123/2026")
        tipo_projeto = col2.selectbox("Tipo de Projeto",
                                      ["Projeto de Lei Ordinária", "Projeto de Emenda", "Resolução", "Decreto"])

        protocolo = st.text_input("Protocolo")
        status_atual = st.selectbox("Status Atual", ["Em Tramitação", "Aprovado", "Rejeitado", "Arquivado"])

        submit_projeto = st.form_submit_button("Gravar Projeto")

        if submit_projeto:
            if numero_ano and protocolo:
                try:
                    data = {
                        "numero_ano_projeto": numero_ano,
                        "tipo_projeto": tipo_projeto,
                        "protocolo": protocolo,
                        "status_atual_projeto": status_atual
                    }
                    # O Supabase gerará a SK_projeto (Identity/Auto-increment) automaticamente
                    response = supabase.table("dim_projetos").insert(data).execute()
                    st.success("✅ Projeto gravado com sucesso! Clique em 'Atualizar' no Power BI para refletir.")
                except Exception as e:
                    st.error(f"Erro ao inserir no banco: {e}")
            else:
                st.warning("Preencha os campos obrigatórios (Número/Ano e Protocolo).")

# ---------------------------------------------------------
# ABA 2: DIM_AUTORES
# ---------------------------------------------------------
with tab_autores:
    st.header("Novo Autor/Parlamentar")
    with st.form("form_autores", clear_on_submit=True):
        nome_autor = st.text_input("Nome Completo do Autor")
        nome_parlamentar = st.text_input("Nome Parlamentar (Como é conhecido)")
        tipo_autor = st.selectbox("Tipo de Autor", ["Vereador", "Comissão", "Mesa Diretora", "Prefeitura"])

        submit_autor = st.form_submit_button("Gravar Autor")

        if submit_autor:
            try:
                data = {
                    "nome_autor": nome_autor,
                    "nome_parlamentar": nome_parlamentar,
                    "tipo_autor": tipo_autor
                }
                supabase.table("dim_autores").insert(data).execute()
                st.success("✅ Autor registrado com sucesso no Data Warehouse.")
            except Exception as e:
                st.error(f"Erro de integração: {e}")

# ---------------------------------------------------------
# ABA 3: FATO_TRAMITACOES
# ---------------------------------------------------------
with tab_tramitacao:
    st.header("Registrar Tramitação")
    st.markdown("Alimenta a tabela `fato_tramitacoes` para análise de gargalos nos setores.")
    with st.form("form_tramitacoes", clear_on_submit=True):
        col1, col2 = st.columns(2)

        # Em um cenário real, esses dados viriam de um 'select' no banco para preencher o combobox
        sk_projeto = col1.number_input("ID do Projeto (SK_projeto)", min_value=1, step=1)
        sk_setor_origem = col2.number_input("ID Setor Origem (SK_setor)", min_value=1, step=1)
        sk_setor_destino = col1.number_input("ID Setor Destino (SK_setor)", min_value=1, step=1)

        data_envio = col2.date_input("Data de Envio")

        submit_tramitacao = st.form_submit_button("Registrar Movimentação")

        if submit_tramitacao:
            try:
                # O cálculo de tempo_em_dias será feito pelo processo de ETL ou View,
                # aqui a interface registra apenas o evento transacional.
                data = {
                    "SK_projeto": sk_projeto,
                    "SK_setor_origem": sk_setor_origem,
                    "SK_setor_destino": sk_setor_destino,
                    "data_envio": data_envio.isoformat(),
                    "quantidade_tramitacoes": 1
                }
                supabase.table("fato_tramitacoes").insert(data).execute()
                st.success("✅ Tramitação registrada. Gargalos já podem ser mensurados no Dashboard.")
            except Exception as e:
                st.error(f"Falha na gravação: Verifique as chaves estrangeiras (FK). Erro: {e}")