import streamlit as st
from core.motor_groq import configurar_inteligencia

st.set_page_config(page_title="Aegis Eleitoral", layout="wide")

st.title("🛡️ Aegis Eleitoral — Inteligência de Campanha")
st.caption("Conexão direta entre geopolítica de dados e marketing político de alta performance.")

# --- OBTER CHAVE DA API DOS SECRETS ---
try:
    api_key = st.secrets["groq_api_key"]
except KeyError:
    st.error("⚠️ Chave de API do Groq não encontrada nos secrets. Configure em `.streamlit/secrets.toml`")
    st.stop()

# --- SIDEBAR: ONBOARDING DO CANDIDATO ---
st.sidebar.title("👤 Perfil do Candidato")

with st.sidebar.form("contexto_campanha"):
    nome = st.text_input("Nome de Urna", placeholder="Ex: Rodrigo Silva")
    idade = st.number_input("Idade", min_value=18, max_value=90, value=42)
    partido = st.text_input("Partido / Federação", placeholder="Ex: MDB")
    
    nicho = st.selectbox("Nicho / Pauta Central", [
        "Agronegócio e Cooperativismo", 
        "Segurança Pública", 
        "Livre Mercado e Empreendedorismo", 
        "Funcionalismo e Educação"
    ])
    
    regioes = st.multiselect("Regiões do RS Prioritárias", [
        "Metropolitana", "Serra", "Planalto", "Norte", "Fronteira Oeste", "Zona Sul"
    ])
    
    ativar_motor = st.form_submit_button("Inicializar Célula Estratégica")

# --- CORPO PRINCIPAL DO APP ---
tab_diagnostico, tab_geopolitica, tab_criativo = st.tabs([
    "🧠 Diagnóstico Inicial", 
    "🗺️ Mapa de Votos", 
    "📝 Fábrica de Conteúdo"
])

# Lógica de ativação após o clique no botão do formulário
if ativar_motor:
    dados_candidato = {"nome": nome, "idade": idade, "partido": partido, "nicho": nicho, "regioes": regioes}
    
    # Guardamos o estado na sessão do Streamlit para persistência entre as abas
    st.session_state['dados_candidato'] = dados_candidato
    st.session_state['motor_ia'] = configurar_inteligencia(api_key, dados_candidato)
    
    st.success(f"✓ Célula de Inteligência ativada para {nome}!")
    
    # Exemplo de uso na primeira aba (Diagnóstico)
    with tab_diagnostico:
        st.subheader("Análise Estratégica Preliminar")
        with st.spinner("O PhD Eleitoral está desenhando o cenário..."):
            # Chamada inicial à IA para gerar as diretrizes de largada
            response = st.session_state['motor_ia'].generate_content(
                "Gere uma análise Swot eleitoral preliminar com base no meu perfil de candidato."
            )
            st.markdown(response.text)
