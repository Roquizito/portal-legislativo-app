# app.py
import streamlit as st
import database as db

st.set_page_config(page_title="Portal de Gestão Legislativa da Câmara Municipal (Mossoró/RN)", page_icon="🏛️", layout="wide")
supabase = db.get_connection()

st.title("🏛️ Portal de Gestão Legislativa da Câmara Municipal (Mossoró/RN)")
st.markdown("---")

tab_projetos, tab_autores, tab_tramitacao = st.tabs([
    "📄 Cadastrar Projeto",
    "👤 Cadastrar Autor",
    "🔄 Registrar Tramitação"
])

# ---------------------------------------------------------
# ABA 1: PROJETOS (Tabela: projeto_lei)
# ---------------------------------------------------------
with tab_projetos:
    st.subheader("Novo Projeto de Lei")
    with st.form("form_projetos", clear_on_submit=True):
        col1, col2 = st.columns(2)
        numero_ano = col1.text_input("Número/Ano do Projeto/Lei*", placeholder="Ex: 123/2026")
        tipo_projeto = col2.selectbox("Tipo de Projeto",
                                      ["Projeto de Lei Ordinária", "Projeto de Emenda", "Resolução", "Decreto"])

        protocolo = col1.text_input("Protocolo*")
        status_atual = col2.selectbox("Status Atual", ["Em Tramitação", "Aprovado", "Rejeitado", "Arquivado"])

        if st.form_submit_button("Gravar Projeto", use_container_width=True):
            try:
                # IMPORTANTE: As chaves deste dicionário devem ter o mesmo nome das colunas lá no Supabase
                payload = {
                    "numero_projeto": numero_ano,
                    "tipo_projeto": tipo_projeto,
                    "protocolo": protocolo,
                    "status_projeto": status_atual
                }
                db.insert_projeto(supabase, payload)
                st.toast("Projeto gravado com sucesso!", icon="✅")
            except Exception as e:
                st.error(f"Erro no banco de dados: {str(e)}")

# ---------------------------------------------------------
# ABA 2: AUTORES (Tabela: autor)
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
                st.toast("Autor cadastrado com sucesso!", icon="✅")
            except Exception as e:
                st.error(f"Erro no banco de dados: {str(e)}")

# ---------------------------------------------------------
# ABA 3: TRAMITAÇÕES (Tabela: tramitacao)
# ---------------------------------------------------------
with tab_tramitacao:
    st.subheader("Registar Movimentação de Setor")

    # Agora procuramos apenas os projetos
    projetos_disponiveis = db.fetch_projetos(supabase)

    if not projetos_disponiveis:
        st.warning("É necessário cadastrar pelo menos um Projeto de Lei antes de registar tramitações.")
    else:
        with st.form("form_tramitacoes", clear_on_submit=True):

            projeto_selecionado = st.selectbox(
                "Selecione o Projeto de Lei*",
                options=projetos_disponiveis,
                format_func=lambda x: f"Projeto {x.get('numero_projeto', x.get('numero', 'Desconhecido'))}"
            )

            col1, col2 = st.columns(2)
            # Substituição dos dropdowns relacionais por campos de texto livre
            origem_texto = col1.text_input("Setor de Origem*", placeholder="Ex: Gabinete 01")
            destino_texto = col2.text_input("Setor de Destino*", placeholder="Ex: Plenário")

            data_envio = st.date_input("Data de Envio")

            if st.form_submit_button("Registar Movimentação", type="primary", use_container_width=True):
                # Validação simples para garantir que os campos não são enviados em branco
                if not origem_texto or not destino_texto:
                    st.error("Por favor, preencha a origem e o destino da tramitação.")
                else:
                    try:
                        id_projeto = projeto_selecionado.get("SK_projeto", projeto_selecionado.get("id"))

                        payload = {
                            "SK_projeto": id_projeto,
                            "origem": origem_texto,  # 👈 Envia o texto escrito pelo utilizador
                            "destino": destino_texto,  # 👈 Envia o texto escrito pelo utilizador
                            "data_envio": data_envio.isoformat(),
                            "quantidade_tramitacoes": 1
                        }
                        db.insert_tramitacao(supabase, payload)
                        st.toast("Tramitação registada com sucesso!", icon="🔄")
                    except Exception as e:
                        st.error(f"Erro de Integração: {str(e)}")