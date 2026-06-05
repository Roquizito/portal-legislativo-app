# app.py
import streamlit as st
import database as db

# Configuração global de UI
st.set_page_config(page_title="Portal de Gestão Legislativa", page_icon="🏛️", layout="wide")
supabase = db.get_connection()

# Construção do Header com UI limpa
st.title("🏛️ Portal de Gestão Legislativa")
st.markdown("---")

# Abas de navegação
tab_projetos, tab_autores, tab_tramitacao = st.tabs([
    "📄 Cadastrar Projeto",
    "👤 Cadastrar Autor",
    "🔄 Registrar Tramitação"
])

# ---------------------------------------------------------
# ABA 1: PROJETOS (Dimensão)
# ---------------------------------------------------------
with tab_projetos:
    st.subheader("Novo Projeto de Lei")
    with st.form("form_projetos", clear_on_submit=True):
        col1, col2 = st.columns(2)
        numero_ano = col1.text_input("Número/Ano do Projeto*", placeholder="Ex: 123/2026")
        tipo_projeto = col2.selectbox("Tipo de Projeto",
                                      ["Projeto de Lei Ordinária", "Projeto de Emenda", "Resolução", "Decreto"])

        protocolo = col1.text_input("Protocolo*")
        status_atual = col2.selectbox("Status Atual", ["Em Tramitação", "Aprovado", "Rejeitado", "Arquivado"])

        if st.form_submit_button("Gravar Projeto no Data Warehouse", use_container_width=True):
            try:
                payload = {
                    "numero_ano_projeto": numero_ano,
                    "tipo_projeto": tipo_projeto,
                    "protocolo": protocolo,
                    "status_atual_projeto": status_atual
                }
                db.insert_projeto(supabase, payload)
                st.toast("Projeto gravado com sucesso!", icon="✅")
            except Exception as e:
                st.error(f"Erro de Validação: {str(e)}")

# ---------------------------------------------------------
# ABA 2: AUTORES (Dimensão)
# ---------------------------------------------------------
with tab_autores:
    st.subheader("Novo Autor/Parlamentar")
    with st.form("form_autores", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nome_autor = col1.text_input("Nome Completo do Autor*")
        nome_parlamentar = col2.text_input("Nome Parlamentar", help="Como é conhecido publicamente")
        tipo_autor = st.selectbox("Tipo de Autor", ["Vereador", "Comissão", "Mesa Diretora", "Prefeitura"])

        if st.form_submit_button("Gravar Autor", use_container_width=True):
            try:
                payload = {
                    "nome_autor": nome_autor,
                    "nome_parlamentar": nome_parlamentar,
                    "tipo_autor": tipo_autor
                }
                db.insert_autor(supabase, payload)
                st.toast("Autor cadastrado e indexado!", icon="✅")
            except Exception as e:
                st.error(f"Erro de Validação: {str(e)}")

# ---------------------------------------------------------
# ABA 3: TRAMITAÇÕES (Fato)
# ---------------------------------------------------------
with tab_tramitacao:
    st.subheader("Registrar Movimentação de Setor")

    # Carregamento dinâmico dos dados para os Dropdowns (UI/UX)
    projetos_disponiveis = db.fetch_projetos(supabase)
    setores_disponiveis = db.fetch_setores(supabase)

    if not projetos_disponiveis or not setores_disponiveis:
        st.warning("É necessário cadastrar Projetos e Setores antes de registrar tramitações.")
    else:
        with st.form("form_tramitacoes", clear_on_submit=True):
            # Selectbox Dinâmico: Mostra o nome legível, mas o código captura o ID (SK)
            projeto_selecionado = st.selectbox(
                "Selecione o Projeto de Lei*",
                options=projetos_disponiveis,
                format_func=lambda x: f"Projeto {x['numero_ano_projeto']}"
            )

            col1, col2 = st.columns(2)
            setor_origem = col1.selectbox(
                "Setor de Origem*",
                options=setores_disponiveis,
                format_func=lambda x: x['nome_setor']
            )
            setor_destino = col2.selectbox(
                "Setor de Destino*",
                options=setores_disponiveis,
                format_func=lambda x: x['nome_setor'],
                index=1 if len(setores_disponiveis) > 1 else 0
            )

            data_envio = st.date_input("Data de Envio do Malote/Documento")

            if st.form_submit_button("Registrar Movimentação na Tabela Fato", type="primary", use_container_width=True):
                try:
                    payload = {
                        "SK_projeto": projeto_selecionado["SK_projeto"],
                        "SK_setor_origem": setor_origem["SK_setor"],
                        "SK_setor_destino": setor_destino["SK_setor"],
                        "data_envio": data_envio.isoformat(),
                        "quantidade_tramitacoes": 1
                    }
                    db.insert_tramitacao(supabase, payload)
                    st.toast(f"Tramitação do projeto {projeto_selecionado['numero_ano_projeto']} registrada!", icon="🔄")
                except Exception as e:
                    st.error(f"Bloqueio de Regra de Negócio: {str(e)}")