# app.py
import streamlit as st
import database as db

st.set_page_config(page_title="Portal de Gestão Legislativa", page_icon="🏛️", layout="wide")
supabase = db.get_connection()

st.title("🏛️ Portal de Gestão Legislativa")
st.markdown("---")

tab_cadastro, tab_tramitacao, tab_parecer = st.tabs([
    "📄 Cadastrar Projeto (Base)",
    "🔄 Atualizar Tramitação",
    "📑 Registar Parecer (Evento)"
])

# ---------------------------------------------------------
# ABA 1: PROJETO E AUTOR (Inserção na Super Tabela)
# ---------------------------------------------------------
with tab_cadastro:
    st.subheader("Génese do Projeto de Lei")

    with st.form("form_central", clear_on_submit=True):
        col1, col2 = st.columns(2)
        st.markdown("#### Identificação do Projeto")
        numero_ano = col1.text_input("Número/Ano*", placeholder="Ex: 123/2026")
        tipo_projeto = col2.selectbox("Tipo de Projeto",
                                      ["Projeto de Lei Ordinária", "Projeto de Emenda", "Resolução", "Decreto"])
        protocolo = col1.text_input("Protocolo*")
        status_atual = col2.selectbox("Status", ["Aguardando Leitura", "Em Tramitação", "Aprovado", "Arquivado"])

        st.markdown("#### Autoria (Propositor)")
        col3, col4 = st.columns([2, 1])
        autor_nome = col3.text_input("Nome do Autor/Órgão*")
        autor_tipo = col4.selectbox("Tipo de Autor", ["Vereador", "Mesa Diretora", "Prefeitura", "Comissão"])

        if st.form_submit_button("Gravar Registo Central", type="primary", use_container_width=True):
            if not numero_ano or not autor_nome:
                st.error("Preencha o Número do Projeto e o Nome do Autor.")
            else:
                try:
                    payload = {
                        "numero_projeto": numero_ano,
                        "tipo_projeto": tipo_projeto,
                        "protocolo": protocolo,
                        "status_atual": status_atual,
                        "autor_nome": autor_nome,
                        "autor_tipo": autor_tipo
                    }
                    db.insert_projeto_central(supabase, payload)
                    st.toast("Projeto e Autor consolidados com sucesso!", icon="✅")
                except Exception as e:
                    st.error(f"Falha de I/O: {str(e)}")

# ---------------------------------------------------------
# ABA 2: TRAMITAÇÃO (Update na Super Tabela)
# ---------------------------------------------------------
with tab_tramitacao:
    st.subheader("Movimentação e Relatoria")

    projetos_disp = db.fetch_projetos(supabase)

    if not projetos_disp:
        st.warning("Cadastre um projeto na aba anterior para gerir a sua localização.")
    else:
        with st.form("form_tramitacao", clear_on_submit=True):
            projeto_selecionado = st.selectbox(
                "Selecione o Projeto*",
                options=projetos_disp,
                format_func=lambda x: f"{x.get('numero_projeto')} - Autoria: {x.get('autor_nome')}"
            )

            col1, col2 = st.columns(2)
            novo_setor = col1.text_input("Novo Setor Atual*", placeholder="Ex: Plenário Principal")
            novo_relator = col2.text_input("Nome do Relator Designado", placeholder="Deixe em branco se não houver")

            if st.form_submit_button("Atualizar Estado", type="primary", use_container_width=True):
                if not novo_setor:
                    st.error("O preenchimento do novo setor é obrigatório.")
                else:
                    try:
                        id_proj = projeto_selecionado.get("id")
                        payload = {
                            "setor_atual": novo_setor,
                            "relator_atual_nome": novo_relator if novo_relator else None
                        }
                        db.update_projeto_localizacao(supabase, id_proj, payload)
                        st.toast("Localização e relatoria atualizadas!", icon="🔄")
                    except Exception as e:
                        st.error(f"Falha de I/O: {str(e)}")

# ---------------------------------------------------------
# ABA 3: PARECER (Insert em Tabela Satélite 1:N)
# ---------------------------------------------------------
with tab_parecer:
    st.subheader("Anexar Parecer de Comissão")
    st.info("Esta operação preserva o histórico. Um projeto pode receber múltiplos pareceres ao longo do tempo.")

    if projetos_disp:
        with st.form("form_parecer", clear_on_submit=True):
            projeto_parecer = st.selectbox(
                "Vincular ao Projeto*",
                options=projetos_disp,
                format_func=lambda x: f"{x.get('numero_projeto')}"
            )

            col1, col2 = st.columns(2)
            comissao = col1.text_input("Comissão Emissora*", placeholder="Ex: CCJR")
            tipo_par = col2.selectbox("Desfecho do Parecer*", ["Favorável", "Contrário", "Com Ressalvas"])
            data_par = st.date_input("Data do Documento")

            if st.form_submit_button("Registar Parecer Histórico", type="primary", use_container_width=True):
                if not comissao:
                    st.error("Informe a comissão que emitiu o parecer.")
                else:
                    try:
                        payload = {
                            "id_projeto": projeto_parecer.get("id"),  # Chave Estrangeira
                            "comissao_emissora": comissao,
                            "tipo_parecer": tipo_par,
                            "data_parecer": data_par.isoformat()
                        }
                        db.insert_parecer(supabase, payload)
                        st.toast("Parecer acoplado à linha do tempo do projeto!", icon="📑")
                    except Exception as e:
                        st.error(f"Falha de I/O: {str(e)}")