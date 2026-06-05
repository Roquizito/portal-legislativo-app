# 🏛️ Diretrizes de Desenvolvimento e Integração da Equipe

Este documento consolida as recomendações arquiteturais e o fluxo de trabalho para o desenvolvimento contínuo do Portal de Gestão Legislativa. O objetivo é garantir que o nosso ambiente de engenharia de software seja replicável, seguro e alinhado às melhores práticas de desenvolvimento.

## 1. Arquitetura e Fluxo de Dados
* Front-end Transacional: A interface é construída em Streamlit (Python). O objetivo desta camada é exclusivamente a captura e validação dos dados dos projetos de lei e tramitações.
* Data Warehouse: O Supabase (PostgreSQL) atua como nosso repositório centralizado na nuvem. As tabelas já estão modeladas em um esquema dimensional (Tabelas Dimensão e Fato).
* Consumo Analítico: O Power BI consumirá as exibições deste banco. Evitemos lógicas de agregação complexas no Python; o cálculo de métricas avançadas deve ser responsabilidade do próprio Banco de Dados ou do Power BI.

## 2. Onboarding: Configuração do Ambiente Local
Para que o Eduardo, o Felipe e qualquer outro membro consigam espelhar o ambiente de desenvolvimento nas suas respectivas máquinas sem atritos de compatibilidade, a seguinte esteira deve ser rigorosamente seguida:
1. Clonar o repositório (`git clone https://github.com/SEU_USUARIO/portal-legislativo-app.git`).
2. Instanciar o ambiente virtual isolado (`python -m venv .venv`).
3. Ativar o ambiente virtual no terminal (`source .venv/bin/activate` para Linux/Mac ou `.venv\Scripts\activate` para Windows).
4. Instalar as dependências estritas do projeto (`pip install -r requirements.txt`).

## 3. Segurança e Gestão de Credenciais
* Vazamento de Dados: É terminantemente proibido o envio de senhas, tokens ou URLs de banco de dados para o repositório remoto.
* Blindagem: O arquivo `.gitignore` já está configurado na raiz do projeto para bloquear a subida da pasta `.streamlit/` e de arquivos de ambiente (`.venv/`, `.idea/`).
* Acesso ao Banco: As credenciais do Supabase devem ser solicitadas de forma privada e inseridas exclusivamente no arquivo local `.streamlit/secrets.toml` de cada desenvolvedor.

## 4. Versionamento e Autenticação (Git/GitHub)
* Assinatura Criptográfica: É altamente recomendada a utilização de chaves GPG para assinar os commits (`git commit -S -m "sua mensagem"`). Isso garante a rastreabilidade, a autenticidade das contribuições e confere o selo "Verified" no GitHub.
* Personal Access Token (PAT): A autenticação via terminal para o envio de código (push) deve ser feita utilizando um PAT gerado nas configurações de desenvolvedor do GitHub (com a permissão 'repo' ativada).
* Sincronização Contínua: Antes de iniciar a codificação de uma nova funcionalidade, executem sempre um `git pull` na branch principal para evitar conflitos de mesclagem (merge conflicts).

## 5. Ferramental Recomendado
* IDE: O uso do PyCharm Professional é recomendado pela sua integração nativa com bancos de dados PostgreSQL (via aba Database). Isso permite a inspeção visual e em tempo real das tabelas (dim_projetos, fato_tramitacoes, etc.) simultaneamente à escrita do código em Python.
* Execução Local: Para rodar a interface gráfica e testar as funcionalidades, utilizem o comando `streamlit run app.py` através do terminal integrado da IDE, sempre certificando-se de que o ambiente virtual está ativo.
