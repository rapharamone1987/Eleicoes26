    import sys
import os
import streamlit as st
from groq import Groq

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="Aegis Eleitoral", layout="wide")

st.title("🛡️ Aegis Eleitoral — Inteligência de Campanha")
st.caption("Conexão direta entre geopolítica de dados e marketing político de alta performance.")

# --- OBTER CHAVE DA API DOS SECRETS ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("⚠️ Chave de API do Groq (GROQ_API_KEY) não encontrada nos secrets do Streamlit Cloud. Configure em Settings → Secrets no painel da nuvem.")
    st.stop()

# --- CÉREBRO INTEGRADO (FUSÃO DO MOTOR DO GROQ NO APP PRINCIPAL) ---
def inicializar_motor_campanha(api_key, dados_candidato):
    """
    Função nativa que substitui o arquivo externo.
    Injeta a doutrina de sistema do PhD e as amarras do TSE direto no chip do Groq.
    """
    client = Groq(api_key=api_key)
    
    nome = dados_candidato.get('nome', 'Candidato')
    partido = dados_candidato.get('partido', 'Partido')
    idade = dados_candidato.get('idade', '45')
    nicho_livre = dados_candidato.get('nicho', 'Geral')
    municipios_texto = ", ".join(dados_candidato.get('municipios', []))

    # Engenharia de Prompt de nível PhD embutida na raiz
    prompt_sistema = f"""
    Você é o Estrategista-Chefe e Consultor de Marketing Político Sênior (nível PhD) da campanha de {nome} ({partido}).
    Cargo Pleiteado: Deputado Federal pelo Rio Grande do Sul (Eleições 2026). Perfil: {idade} anos.
    
    [MATRIZ GEOPOLÍTICA E NARRATIVA]
    - Território de Operação: {municipios_texto}
    - Nicho Ideológico / Pauta Central: {nicho_livre}
    
    [DIRETRIZES DO COMITÊ CENTRAL - OBRIGATÓRIO]
    1. TOM E POSTURA: Responda com pragmatismo, altivez e profundidade técnica. O eleitor gaúcho é altamente politizado. Evite clichês genéricos.
    2. MICROSEGMENTAÇÃO: Amarre a pauta de "{nicho_livre}" diretamente às dores locais de {municipios_texto}.
    3. TRAVA JURÍDICA DE COMPLIANCE (TSE): Proibido usar pedidos explícitos de voto ("vote em mim"). Use termos institucionais ("Defendo que", "Precisamos debater").
    """

    class EngineLocal:
        def generate_content(self, prompt_usuario):
            completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": prompt_usuario}
                ],
                temperature=0.3,
                max_tokens=2048
            )
            class Obj:
                def __init__(self, text): self.text = text
            return Obj(completion.choices[0].message.content)
            
    return EngineLocal()

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

# PROCESSAMENTO DO DISPARO
if activar_motor:
    dados_candidato = {"nome": nome, "idade": idade, "partido": partido, "nicho": nicho, "municipios": municipios_alvo}
    st.session_state['dados_candidato'] = dados_candidato
    st.session_state['motor_ia'] = inicializar_motor_campanha(api_key, dados_candidato)
    
    with st.spinner("O PhD Eleitoral está desenhando o cenário..."):
        try:
            response = st.session_state['motor_ia'].generate_content(
                "Gere uma análise SWOT eleitoral preliminar sucinta em tópicos com base no meu perfil de candidato."
            )
            st.session_state['analise_inicial'] = response.text
        except Exception as e:
            st.error(f"Erro na API do Groq: {e}")

# EXIBIÇÃO PERSISTENTE DAS TELAS
if 'motor_ia' in st.session_state:
    dados_usuario = st.session_state['dados_candidato']
    
    # --- ABA 1: DIAGNÓSTICO ---
    with tab_diagnostico:
        st.subheader(f"Análise Estratégica Preliminar — {dados_usuario['nome']}")
        st.markdown(st.session_state.get('analise_inicial', 'Carregando análise...'))
        
    # --- ABA 2: CONVERSÃO DE LIDERANÇAS ---
    with tab_conversao:
        st.header("🗺️ Análise de Conversão Territorial")
        st.markdown("Cruze os indicadores socioeconômicos locais com as metas estruturais de cabos eleitorais.")
        
        cidade_foco = st.selectbox("Selecione o município para auditoria tática:", options=dados_usuario['municipios'])
        
        if cidade_foco in ["PASSO FUNDO", "ERECHIM"]:
            perfil_cidade = {
                "perfil": "Polo de Serviços, Saúde e Agronegócio de Precisão do Planalto Médio.",
                "votos_validos": 120000,
                "pauta_urgente": "Infraestrutura rodoviária secundária (escoamento) e segurança contra invasão de propriedades rurais."
            }
        elif cidade_foco in ["PORTO ALEGRE", "CAXIAS DO SUL"]:
            perfil_cidade = {
                "perfil": "Eixo Urbano Adensado, Forte apelo no Setor Terciário, Indústria e Serviços de Tecnologia.",
                "votos_validos": 800000,
                "pauta_urgente": "Cercamento eletrônico comercial, redução de furtos em centros urbanos e mobilidade."
            }
        else:
            perfil_cidade = {
                "perfil": "Fronteira Oeste, Conexão de Logística Internacional do Mercosul. Base pecuária e lavoura de arroz.",
                "votos_validos": 75000,
                "pauta_urgente": "Apoio ao policiamento ostensivo de fronteira e desburocratização tributária do produtor."
            }
            
        col_socio1, col_socio2 = st.columns(2)
        with col_socio1:
            st.info(f"**Matriz Econômica:** {perfil_cidade['perfil']}\n\n**Demanda Crítica Local:** *{perfil_cidade['pauta_urgente']}*")
        with col_socio2:
            st.metric("Eleitorado Válido Estimado", f"{perfil_cidade['votos_validos']:} Votos")

        st.markdown("---")
        st.subheader("🧮 Calculadora de Retorno por Liderança (CRM)")
        
        col_crm1, col_crm2, col_crm3 = st.columns(3)
        with col_crm1:
            num_liderancas = st.number_input("Número de Líderes Grandes na Cidade", min_value=0, max_value=100, value=5)
        with col_crm2:
            media_votos_lider = st.number_input("Meta de Entrega por Líder (Votos)", min_value=10, max_value=5000, value=1200)
        with col_crm3:
            votos_opiniao_insta = st.slider("Votos de Opinião via Tráfego Pago", min_value=0, max_value=20000, value=2000)
            
        votos_estrutura_total = num_liderancas * media_votos_lider
        votos_projetados_totais = votos_estrutura_total + votos_opiniao_insta
        share_votos = (votos_projetados_totais / perfil_cidade['votos_validos']) * 100
        
        st.markdown("#### 🏁 Projeção de Desempenho Local")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Votos de Estrutura", f"{votos_estrutura_total:}")
        col_m2.metric("Total de Votos Projetados", f"{votos_projetados_totais:}")
        col_m3.metric("Share do Eleitorado Local", f"{share_votos:.2f}%")
        
        if st.button(f"🧠 Gerar Relatório de Viabilidade para {cidade_foco}"):
            with st.spinner("Analisando consistência tática e cobrando as bases..."):
                prompt_analise = f"""
                Analise o cenário do candidato na cidade de {cidade_foco}.
                Perfil Socioeconômico do município: {perfil_cidade['perfil']}
                Demanda Crítica local: {perfil_cidade['pauta_urgente']}
                Meta de Votos Estruturais: {votos_estrutura_total} votos através de {num_liderancas} líderes.
                Meta de Votos de Opinião (Redes): {votos_opiniao_insta} votos.
                
                Forneça um diagnóstico respondendo em tópicos claros:
                1. A meta de votos por líder ({media_votos_lider}) é estatisticamente viável ou inflacionada para a realidade da cidade?
                2. Como o candidato deve amarrar a sua pauta principal de "{dados_usuario['nicho']}" à dor real de "{perfil_cidade['pauta_urgente']}" para cobrar desempenho dessas lideranças?
                3. Qual a recomendação de tráfego pago para arrastar o voto de opinião local?
                """
                try:
                    relatorio_cidade = st.session_state['motor_ia'].generate_content(prompt_analise)
                    st.session_state[f'relatorio_{cidade_foco}'] = relatorio_cidade.text
                except Exception as e:
                    st.error(f"Erro no motor: {e}")
                    
        if f'relatorio_{cidade_foco}' in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state[f'relatorio_{cidade_foco}'])

    # --- ABA 3: FÁBRICA DE POSTS ---
    with tab_criativo:
        st.header("📝 Fábrica de Conteúdo com Guardrails Jurídicos")
        st.markdown("Gere peças de comunicação contextualizadas ao território e imunes a sanções do TSE.")
        
        st.markdown(
            f"""
            <div style="background-color: #F0F2F6; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                <strong>Briefing Ativo:</strong> {dados_usuario['nome']} | Pauta: {dados_usuario['nicho']}
            </div>
            """, unsafe_allow_html=True
        )
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            canal = st.selectbox("Formato do Post", ["Roteiro de Vídeo Curto (Reels)", "Carrossel Informativo (Tópicos)", "Nota Oficial de Imprensa"])
        with col_c2:
            cidade_recorte = st.selectbox("Afunilar Narrativa para qual Cidade?", ["Foco Geral"] + dados_usuario['municipios'])
            
        pauta_dia = st.text_area("Fato político ou notícia do dia para rebater/apoiar:", placeholder="Ex: O aumento nos índices de criminalidade rural.")
        
        if st.button("🚀 Disparar Fábrica de Criativos"):
            if not pauta_dia:
                st.error("Insira uma pauta para orientar a redação.")
            else:
                with st.spinner("Redigindo peça institucional..."):
                    prompt_criativo = f"""
                    Gere uma peça no formato [{canal}] com foco territorial em [{cidade_recorte}].
                    Fato do dia a abordar: "{pauta_dia}".
                    Divida a resposta estruturalmente (Hook/Gancho, o desenvolvimento do argumento e a legenda sugerida). Aplique as travas de compliance eleitoral do seu sistema.
                    """
                    try:
                        peca_final = st.session_state['motor_ia'].generate_content(prompt_criativo)
                        st.session_state['peca_comunicacao_atual'] = peca_final.text
                    except Exception as e:
                        st.error(f"Erro na fábrica de criativos: {e}")
                        
        if 'peca_comunicacao_atual' in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state['peca_comunicacao_atual'])

else:
    with tab_diagnostico:
        st.info("👋 Central de comando aguardando inicialização. Preencha o Perfil do Candidato na barra lateral e clique em 'Inicializar Célula Estratégica' para começar.")
