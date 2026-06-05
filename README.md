# 🏛️ Portal de Gestão Legislativa - Data Warehouse (DW)

Este repositório contém a camada de interface transacional do **Portal de Gestão Legislativa**, desenvolvido em Python utilizando **Streamlit**. O sistema foi projetado para atuar como o front-end transacional alimentando diretamente um repositório centralizado na nuvem (**Supabase/PostgreSQL**), estruturado sob a modelagem dimensional de um Data Warehouse (DW) para posterior consumo e análise analítica via **Power BI**.

---

## 🗺️ Visão Geral da Arquitetura

A arquitetura do sistema é dividida em três camadas fundamentais:

1. **A Interface (Front-End Transacional):** Desenvolvida em Streamlit (Python), permite a inserção, atualização e validação de projetos de lei, autores/parlamentares e o registro de eventos de tramitação de forma intuitiva.
2. **O Servidor de Banco de Dados (Storage & DW):** Hospedado no Supabase (PostgreSQL), armazena as dimensões e tabelas fatos, garantindo a consistência relacional e integridade referencial através de restrições de chaves estrangeiras (FK).
3. **O Dashboard (Analytics):** Conectado diretamente ao Supabase para atualização em tempo real ou agendada, consolidando as métricas de produtividade e tramitações legislativas.

---

## 📊 Estrutura de Modelagem Dimensional (DW)

O banco de dados foi populado e estruturado com base no histórico real de proposições legislativas (incluindo dados históricos de comissões, pareceres e votações). O esquema relacional implementa as seguintes tabelas:

### Tabelas Dimensionais
* **`dim_projetos`**: Controla o ciclo de vida das proposições.
    * `SK_projeto` (SERIAL PRIMARY KEY): Chave substituta (*Surrogate Key*).
    * `numero_ano_projeto`: Identificador de negócio (Ex: `176/2017`).
    * `tipo_projeto`: Tipo da proposição (Ex: `Projeto de Lei Ordinária`).
    * `protocolo`: Código de registro transacional (Ex: `0004061`).
    * `status_atual_projeto`: Estado corrente (Ex: `Virou lei`, `Arquivado`, `Em Tramitação`).
    * `num_lei_gerada`: Número da lei caso aprovada (se não, `NULL`).
    * `data_publicacao`: Data em que virou lei (se não, `NULL`).
* **`dim_autores`**: Cadastro de parlamentares e entidades proponentes.
    * `SK_autor` (SERIAL PRIMARY KEY)
    * `nome_autor`: Nome completo do proponente.
    * `nome_parlamentar`: Nome político/parlamentar.
    * `tipo_autor`: Categoria (Ex: `Vereador`, `Mesa Diretora`, `Comissão`).
* **`dim_setores`**: Mapeamento das comissões e órgãos internos.
    * `SK_setor` (SERIAL PRIMARY KEY)
    * `nome_setor`: Nome descritivo (Ex: `Comissão de Constituição, Justiça e Redação`).
    * `codigo_interno`: Sigla ou abreviação técnica (Ex: `CCJR`).

### Tabela Fato
* **`fato_tramitacoes`**: Mede o fluxo e gargalos dos projetos pelos setores da Casa Legislativa.
    * `id_tramitacao` (SERIAL PRIMARY KEY)
    * `SK_projeto` (INTEGER REFERENCES `dim_projetos`)
    * `SK_setor_origem` (INTEGER REFERENCES `dim_setores`)
    * `SK_setor_destino` (INTEGER REFERENCES `dim_setores`)
    * `data_envio`: Data em que a movimentação foi registrada.
    * `quantidade_tramitacoes`: Métrica agregada (padrão `1` por registro).

---

## 🚀 Como Rodar o Projeto na sua Máquina

Siga o passo a passo técnico abaixo para replicar o ambiente de desenvolvimento localmente.

### 1. Pré-requisitos
Certifique-se de ter instalado em seu sistema operacional (Linux/Pop!_OS/Windows):
* Python 3.10 ou superior
* Git

### 2. Clonar o Repositório
No terminal da sua máquina ou da sua IDE (PyCharm/VS Code), execute:
```bash
git clone [https://github.com/Roquizito/portal-legislativo-app.git](https://github.com/Roquizito/portal-legislativo-app.git)
cd portal-legislativo-app
3. Configurar o Ambiente Virtual (.venv)
É fundamental isolar as dependências do projeto para evitar conflitos globais:

Bash
# Criar o ambiente virtual
python -m venv .venv

# Ativar no Linux (Pop!_OS / Zorin OS / Ubuntu)
source .venv/bin/activate

# Ativar no Windows (Prompt de Comando)
.venv\Scripts\activate
4. Instalar Dependências
Com o ambiente virtual ativo (indicado por (.venv) no início do prompt do terminal), instale os pacotes necessários listados no requirements.txt:

Bash
pip install -r requirements.txt
5. Configurar Chaves de Acesso Seguras (Secrets)
O Streamlit utiliza um gerenciador interno de credenciais. Nunca faça commits contendo senhas e chaves de API.

Crie um diretório chamado .streamlit na raiz do projeto.

Dentro dele, crie um arquivo chamado secrets.toml.

Insira as variáveis obtidas no painel do Supabase (Project Settings > API):

Ini, TOML
# .streamlit/secrets.toml
SUPABASE_URL = "[https://seu-subdominio.supabase.co](https://seu-subdominio.supabase.co)"
SUPABASE_KEY = "sua-anon-public-key-gerada"
🛠️ Execução e Testes
Para inicializar o servidor web de desenvolvimento do Streamlit, execute:

Bash
streamlit run app.py
A aplicação abrirá automaticamente no seu navegador padrão pelo endereço local http://localhost:8501.

💡 Dica de Integração com o PyCharm Professional
Para inspecionar as inserções de dados em tempo real sem precisar sair do ambiente de código:

Abra a aba Database no canto direito do PyCharm.

Adicione uma conexão PostgreSQL.

Utilize as credenciais de conexão direta fornecidas na aba Database Settings do painel do Supabase.

🔒 Boas Práticas de Versionamento (Git & Equipe)
Para garantir um fluxo de trabalho profissional e seguro entre todos os colaboradores do grupo:

Proteção de Arquivos: O arquivo .gitignore já está configurado para blindar pastas locais de configuração de IDEs (.idea/), ambientes virtuais (.venv/) e chaves secretas (secrets.toml). Nunca force a subida destes arquivos.

Assinatura Criptográfica (GPG): Os commits deste repositório utilizam assinatura criptográfica GPG para validação de autoria e identidade no GitHub (selo Verified). Certifique-se de que sua chave pública antiga ou nova esteja devidamente importada e vinculada ao Git global:

Bash
git config --global user.signingkey SEU_ID_DE_CHAVE
Atualizações Remotas: Antes de iniciar o desenvolvimento de uma nova funcionalidade, realize um git pull para sincronizar seu histórico local com as últimas alterações enviadas pela equipe.

🏛️ Desenvolvido como projeto de modelagem avançada de banco de dados e engenharia de software.
