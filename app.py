import sys
import os

# Trava de segurança de caminhos para o servidor Linux da nuvem
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

st.set_page_config(page_title="Aegis Eleitoral", layout="wide")

# --- TESTE DE SANIDADE DAS PASTAS ---
# Tentamos importar estritamente da pasta ESSENCIAL. Não existe palavra 'core' aqui.
try:
    from essencial.motor_groq import configurar_inteligencia
    motor_disponivel = True
except ModuleNotFoundError as e:
    motor_disponivel = False
    erro_detalhado = str(e)

st.title("🛡️ Aegis Eleitoral — Inteligência de Campanha")
st.caption("Conexão direta entre geopolítica de dados e marketing político de alta performance.")

# Se o Python reclamar de caminhos, o app não fica preto, ele mostra este aviso claro:
if not motor_disponivel:
    st.error("❌ ERRO CRÍTICO DE INFRAESTRUTURA NO GITHUB")
    st.markdown(
        f"""
        O servidor do Streamlit não encontrou o motor na pasta correta.
        
        **O que o sistema reportou:** `{erro_detalhado}`
        
        **Como resolver no GitHub:**
        1. Certifique-se de que a pasta no seu repositório chama-se exatamente `essencial` (com todas as letras minúsculas).
        2. Verifique se o arquivo `motor_groq.py` está dentro dela.
        3. Garanta que o arquivo `__init__.py` (em branco) também está dentro da pasta `essencial`.
        """
    )
    st.stop()

# --- OBTER CHAVE DA API DOS SECRETS ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("⚠️ Chave de API do Groq (GROQ_API_KEY) não encontrada nos secrets do Streamlit Cloud.")
    st.stop()

# --- LISTA DE MUNICÍPIOS FILTRADOS ---
MUNICIPACIOS_RS = ["PORTO ALEGRE", "CAXIAS DO SUL", "PELOTAS", "SANTA MARIA", "PASSO FUNDO", "URUGUAIANA", "ERECHIM", "BAGÉ"]

# --- SIDEBAR: ONBOARDING DO CANDIDATO ---
st.sidebar.title("👤 Perfil do Candidato")

with st.sidebar.form("contexto_campanha"):
    nome = st.text_input("Nome de Urna", value="Tenente Ramos")
    idade = st.number_input("Idade", min_value=18, max_value=90, value=45)
    partido = st.text_input("Partido / Federação", value="PL")
    nicho = st.text_input("Nicho / Pauta Central", value="Segurança Pública e Combate ao Roubo de Carga")
    municipios_alvo = st.multiselect("Municípios Alvo", options=MUNICIPACIOS_RS, default=["PORTO ALEGRE", "PASSO FUNDO"])
    
    ativar_motor = st.form_submit_button("Inicializar Célula Estratégica")

# --- ABAS OPERACIONAIS ---
tab_diagnostico, tab_conversao, tab_criativo = st.tabs([
    "🧠 Diagnóstico Inicial", 
    "🗺️ Inteligência Territorial e Lideranças", 
    "📝 Fábrica de Conteúdo"
])

# PROCESSAMENTO DO BOTÃO
if activar_motor:
    dados_candidato = {"nome": nome, "idade": idade, "partido": partido, "nicho": nicho, "municipios": municipios_alvo}
    st.session_state['dados_candidato'] = dados_candidato
    st.session_state['motor_ia'] = configurar_inteligencia(api_key, dados_candidato)
    
    with st.spinner("O PhD Eleitoral está desenhando o cenário..."):
        try:
            response = st.session_state['motor_ia'].generate_content(
                "Gere uma análise SWOT eleitoral preliminar sucinta em tópicos com base no meu perfil."
            )
            st.session_state['analise_inicial'] = response.text
        except Exception as e:
            st.error(f"Erro na API do Groq: {e}")

# EXIBIÇÃO PERSISTENTE DAS TELAS
if 'motor_ia' in st.session_state:
    dados_usuario = st.session_state['dados_candidato']
    
    with tab_diagnostico:
        st.subheader(f"Análise Estratégica Preliminar — {dados_usuario['nome']}")
        st.markdown(st.session_state.get('analise_inicial', 'Carregando...'))
        
    with tab_conversao:
        st.subheader("🗺️ Mapeamento e Metas Territoriais")
        st.info("Painel de controle de cabos eleitorais pronto para receber dados.")
        
    with tab_criativo:
        st.subheader("📝 Fábrica de Posts")
        st.info("Módulo pronto para receber pautas diárias.")
else:
    with tab_diagnostico:
        st.info("👋 Central de comando aguardando inicialização na barra lateral.")
