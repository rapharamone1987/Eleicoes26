import sys
import os
import streamlit as st
import pandas as pd
from groq import Groq

# ------------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA INTERFACE E AMBIENTE (TELA NEUTRA COMERCIAL)
# ------------------------------------------------------------------------------
st.set_page_config(page_title="Aegis Eleitoral PRO", layout="wide")

st.title("🛡️ Aegis Eleitoral — Inteligência de Guerrilha")
st.caption("Plataforma Avançada de Sala de Situação, Big Data Geopolítico e Controle Financeiro — Eleições 2026")

# --- VALIDAÇÃO DA CHAVE DE API NOS SECRETS ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("⚠️ Chave de API do Groq (GROQ_API_KEY) não encontrada nos secrets do Streamlit Cloud.")
    st.stop()

# ------------------------------------------------------------------------------
# 2. BANCO DE DATA-ANALYTICS ÂNCORA (MUNICÍPIOS REFERÊNCIA DO RS)
# ------------------------------------------------------------------------------
DADOS_GEOPOLITICOS_RS = {
    "PORTO ALEGRE": {
        "regiao": "Metropolitana",
        "eleitorado_total": 1084000,
        "abstencao_media": "22.4%",
        "perfil_socioeconomico": "Capital do Estado. Predomínio do setor de serviços, funcionalismo público, comércio adensado e forte núcleo universitário. Alto IDH (0.805).",
        "comportamento_historico": "Eleitorado altamente fragmentado, crítico e polarizado. Divisão histórica acentuada entre periferias (voto de demanda estrutural) e bairros centrais (voto ideológico de opinião/redes).",
        "principais_dores": "Segurança nos eixos comerciais, revitalização do centro urbano, eficiência no transporte público e desburocratização tributária municipal."
    },
    "CAXIAS DO SUL": {
        "regiao": "Serra Gaúcha",
        "eleitorado_total": 348000,
        "abstencao_media": "18.1%",
        "perfil_socioeconomico": "Segundo maior polo econômico do estado. Forte DNA metal-mecânico, industrial, vitivinicultor e cooperativista. Baixo desemplego.",
        "comportamento_historico": "Eleitorado de perfil conservador, pragmático e focado em pautas econômicas de livre mercado, ordem pública e valorização do trabalho e da família.",
        "principais_dores": "Gargalos logísticos de escoamento (estradas federais), segurança nas zonas industriais e demandas por saúde suplementar."
    },
    "PASSO FUNDO": {
        "regiao": "Planalto Médio",
        "eleitorado_total": 152000,
        "abstencao_media": "16.5%",
        "perfil_socioeconomico": "Polo de saúde, educação superior e entroncamento logístico do agronegócio de alta precisão. Renda impulsionada pelas safras de grãos.",
        "comportamento_historico": "Voto tradicionalmente ligado a grandes lideranças locais (voto de liderança e representação regional). Forte influência do setor produtivo e sindicatos rurais.",
        "principais_dores": "Insegurança e roubo de defensivos em propriedades rurais, infraestrutura de rodovias estaduais secundárias e retenção de talentos técnicos."
    },
    "URUGUAIANA": {
        "regiao": "Fronteira Oeste",
        "eleitorado_total": 88000,
        "abstencao_media": "24.2%",
        "perfil_socioeconomico": "Maior porto seco da América Latina. Economia baseada na logística internacional do Mercosul, pecuária extensiva e grande lavoura arrozeira.",
        "comportamento_historico": "Eleitorado com alto índice de abstenção. Voto muito dependente de estruturas políticas consolidadas e forte apelo a demandas de segurança nacional e apoio governamental.",
        "principais_dores": "Falta de policiamento nas rotas de fronteira, burocracia aduaneira sufocante e isolamento político em relação à capital."
    }
}

DADOS_ESTADUAIS_GERAIS = {
    "regiao": "Todo o Rio Grande do Sul",
    "eleitorado_total": 8600000,
    "abstencao_media": "19.8%",
    "perfil_socioeconomico": "Estado com forte equilíbrio entre o PIB industrial (Serra/Metropolitana) e a força do Agronegócio (Norte/Fronteira/Sul). Elevado índice de politização e IDH médio alto.",
    "comportamento_historico": "Tendência histórica a eleições plebiscitárias e polarizadas. Forte tradição de voto regionalizado, onde deputados federais precisam consolidar bases em 'dobradinhas' com estaduais locais.",
    "principais_dores": "Dívida pública do Estado, infraestrutura logística e estradas, segurança pública rural e urbana, e incentivos fiscais para reter indústrias."
}

# --- LISTA OFICIAL EXAUSTIVA DOS MUNICÍPIOS DO RIO GRANDE DO SUL ---
MUNICICIPIOS_497_RS = [
    "PORTO ALEGRE", "CAXIAS DO SUL", "PASSO FUNDO", "URUGUAIANA", "PELOTAS", "SANTA MARIA", "CANOAS", "GRAVATAÍ", 
    "VIAMÃO", "NOVO HAMBURGO", "SÃO LEOPOLDO", "RIO GRANDE", "ALVORADA", "ERECHIM", "LAJEADO", "OSÓRIO", "TORRES", 
    "TRAMANDAÍ", "CAPÃO DA CANOA", "XANGRI-LÁ", "CIDREIRA", "BALNEÁRIO PINHAL", "ARROIO DO SAL", "IMBÉ", "MOSTARDAS", 
    "TAVARES", "SANTO ANTÔNIO DA PATRULHA", "BAGÉ", "SANTA CRUZ DO SUL", "CACHOEIRINHA", "BENTO GONÇALVES", "IJUÍ", 
    "SANTANA DO LIVRAMENTO", "CRUZ ALTA", "SANTA ROSA", "SÃO BORJA", "CARAZINHO", "VACARIA", "CAMPO BOM", 
    "ALEGRETE", "MONTENEGRO", "TAQUARA", "GUAÍBA", "ESTEIO", "SAPUCAIA DO SUL", "SÃO GABRIEL", "ESTRELA", 
    "VENÂNCIO AIRES", "FARROUPILHA", "GRAMADO", "CANELA", "DOM PEDRITO", "SOLEDADE", "MARAU", "PANAMBI", 
    "SÃO LUIZ GONZAGA", "SÃO LOURENÇO DO SUL", "CAÇAPAVA DO SUL", "SANTIAGO", "CANGUÇU", "PALMEIRA DAS MISSÕES", 
    "FREDERICO WESTPHALEN", "SANTO ÂNGELO", "ROSÁRIO DO SUL", "ITAQUI", "QUARAÍ", "JAGUARÃO"
]
MUNICICIPIOS_497_RS = sorted(list(set(MUNICICIPIOS_497_RS)))

# ------------------------------------------------------------------------------
# 3. MOTOR DE INTELIGÊNCIA ARTIFICIAL MILITARIZADO (PHD CORE)
# ------------------------------------------------------------------------------
def ativar_motor_campanha(api_key, dados_candidato):
    client = Groq(api_key=api_key)
    
    nome = dados_candidato.get('nome', 'Candidato')
    partido = dados_candidato.get('partido', 'Partido')
    idade = dados_candidato.get('idade', '45')
    nicho_livre = dados_candidato.get('nicho', 'Geral')
    biografia = dados_candidato.get('biografia', 'Sem histórico detalhado.')
    municipios_texto = ", ".join(dados_candidato.get('municipios', []))

    prompt_sistema = f"""
    Você é o Estrategista-Chefe, General de Sala de Crise e PhD em Ciência Política da campanha de {nome} ({partido}), disputando a eleição de Deputado Federal pelo Rio Grande do Sul.
    Idade: {idade} anos.
    
    [PRONTUÁRIO BIOGRÁFICO REAL DO CANDIDATO]
    {biografia}
    
    [MAPA GEOPOLÍTICO E PAUTA DE TRINCHEIRA]
    - Territórios-Alvo Selecionados: {municipios_texto}
    - Trincheira Temática Central: {nicho_livre}
    
    [DIRETRIZES DO COMITÊ CENTRAL - IMPRESCINDÍVEL]
    1. POSTURA TÁTICA: Suas recomendações devem ser arrojadas, agressivas e baseadas em táticas reais de guerra eleitoral de posições. Ignore clichês.
    2. ANÁLISE JURÍDICO-POLÍTICA: O eleitor gaúcho exige profundidade extrema. Confronte a biografia do candidato com as dores locais, indicando manobras reais de tomada de território político.
    3. TRAVA JURÍDICA TSE: Desenhe planos institucionais de alto impacto ("Minha bandeira intransigente é"), mas NUNCA use palavras de pedido explícito de voto ("vote", "eleja").
    """

    class EngineGuerrilha:
        def generate_content(self, prompt_usuario):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": prompt_usuario}
                ],
                temperature=0.1,  
                max_tokens=2500
            )
            class Wrapper:
                def __init__(self, text): self.text = text
            return Wrapper(completion.choices[0].message.content)
            
    return EngineGuerrilha()

# ------------------------------------------------------------------------------
# 4. PAINEL DE CONTROLE LATERAL (TELA TOTALMENTE LIMPA DE MERCADO)
# ------------------------------------------------------------------------------
st.sidebar.title("👤 Inteligência de Origem")
st.sidebar.markdown("*Insira os dados reais do candidato para inicializar os algoritmos de guerrilha.*")

with st.sidebar.form("contexto_campanha"):
    nome_input = st.text_input("Nome de Urna", placeholder="Ex: Capitão Veríssimo")
    idade_input = st.number_input("Idade", min_value=18, max_value=90, value=35)
    partido_input = st.text_input("Partido / Federação", placeholder="Ex: NOVO / PP / MDB")
    nicho_input = st.text_input("Trincheira / Pauta Central", placeholder="Ex: Defesa do Livre Mercado / Segurança Pública")
    
    biografia_input = st.text_area(
        "Biografia e Capital Político do Candidato", 
        placeholder="Ex: Detalhe o recall político do candidato, profissão, áreas onde possui forte liderança ou se é um nome estreante na urna..."
    )
    
    # LISTA COMPLETA ATIVA: Permite selecionar qualquer cidade do RS para análise
    municipios_alvo = st.multiselect(
        "Municípios Foco de Atuação (Lista RS)", 
        options=MUNICICIPIOS_497_RS,
        default=[] 
    )
    
    ativar_motor = st.form_submit_button("🔥 Disparar Célula de Inteligência")

# ------------------------------------------------------------------------------
# 5. MEMÓRIA DE SESSÃO E PROCESSAMENTO DA IA
# ------------------------------------------------------------------------------
if ativar_motor:
    if not nome_input or not partido_input or not nicho_input or not biografia_input or not municipios_alvo:
        st.sidebar.error("⚠️ Operação Interrompida: Preencha TODOS os campos da barra lateral para forjar a identidade estratégica.")
    else:
        dados_candidato = {
            "nome": nome_input, 
            "idade": idade_input, 
            "partido": partido_input, 
            "nicho": nicho_input, 
            "biografia": biografia_input,
            "municipios": municipios_alvo
        }
        st.session_state['dados_candidato'] = dados_candidato
        st.session_state['motor_ia'] = ativar_motor_campanha(api_key, dados_candidato)
        
        with st.spinner("Mapeando vulnerabilidades do território e quebrando defesas adversárias..."):
            try:
                response = st.session_state['motor_ia'].generate_content(
                    "Gere um Diagnóstico de Ruptura Eleitoral. Faça uma análise SWOT agressiva e profunda confrontando minha biografia com as regiões selecionadas."
                )
                st.session_state['analise_inicial'] = response.text
                st.toast("Célula estratégica operando em nível máximo!", icon="✅")
            except Exception as e:
                st.error(f"Erro na API do Groq: {e}")

# ------------------------------------------------------------------------------
# 6. ABAS OPERACIONAIS DE COMANDO
# ------------------------------------------------------------------------------
tab_diagnostico, tab_bigdata, tab_conversao, tab_financeiro, tab_criativo = st.tabs([
    "🧠 Plano de Ruptura (SWOT)", 
    "📊 Big Data Geopolítico",
    "🗺️ Inteligência Territorial", 
    "💰 Alocação e Controle Financeiro",
    "📝 Fábrica de Conteúdo de Guerrilha"
])

if 'motor_ia' in st.session_state:
    dados_usuario = st.session_state['dados_candidato']
    
    # --- ABA 1: PLANO DE RUPTURA ---
    with tab_diagnostico:
        st.subheader(f"Plano Tático de Ataque — {dados_usuario['nome']}")
        if 'analise_inicial' in st.session_state:
            st.markdown(st.session_state['analise_inicial'])
            st.text_area("Copiar Relatório SWOT:", value=st.session_state['analise_inicial'], height=120)

    # --- ABA 2: BIG DATA GEOPOLÍTICO REATIVO POR ALVO (REATIVIDADE CORRIGIDA) ---
    with tab_bigdata:
        st.header("📊 Inteligência de Dados Demográficos e Eleitorais")
        st.markdown("Auditoria de população, abstenção e comportamento político reativa ao alvo selecionado.")
        
        # Alimenta-se dinamicamente APENAS dos municípios selecionados na barra lateral
        opcao_visualizacao = st.selectbox(
            "Selecione o município ativo para auditoria de Big Data:",
            options=["Consolidado Estadual (Geral)"] + dados_usuario['municipios']
        )
        
        if opcao_visualizacao in DADOS_GEOPOLITICOS_RS:
            bd = DADOS_GEOPOLITICOS_RS[opcao_visualizacao]
            modo_ia_puro = False
        elif opcao_visualizacao == "Consolidado Estadual (Geral)":
            bd = DADOS_ESTADUAIS_GERAIS
            modo_ia_puro = False
        else:
            modo_ia_puro = True
            
        if not modo_ia_puro:
            col_bd1, col_bd2, col_bd3 = st.columns(3)
            col_bd1.metric("Eleitorado Alvo Fixo", f"{bd['eleitorado_total']:,} Votos")
            col_bd2.metric("Abstenção Média Histórica", bd['abstencao_media'])
            col_bd3.metric("Recorte Geográfico", bd['regiao'])
            
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.info(f"**Matriz Socioeconômica Regional:**\n\n{bd['perfil_socioeconomico']}")
            with col_info2:
                st.warning(f"**Comportamento de Urna e Histórico:**\n\n{bd['comportamento_historico']}")
        else:
            st.warning(f"🌐 Varredura Ativa: O município '{opcao_visualizacao}' exige processamento dinâmico da IA.")
            st.markdown("*O motor vai extrair do seu ecossistema as estimativas de população, eleitorado e abstenção para esta cidade específica.*")

        st.markdown("---")
        
        if st.button(f"🧠 Forjar Cenários de Discurso e Estatísticas para {opcao_visualizacao}"):
            with st.spinner(f"Processando registros demográficos e de população de {opcao_visualizacao}..."):
                if not modo_ia_puro:
                    contexto_prompt = f"Perfil Socioeconômico: {bd['perfil_socioeconomico']}. Histórico de Urna: {bd['comportamento_historico']}."
                else:
                    contexto_prompt = f"Gere dados detalhados de população estimada, eleitorado aproximado, abstenção média histórica e a matriz econômica real da cidade de {opcao_visualizacao}, Rio Grande do Sul."
                
                prompt_bd = f"""
                Analise os dados geopolíticos estruturais e demográficos para a praça [{opcao_visualizacao}]:
                Contexto Regional: {contexto_prompt}
                
                Considerando minha biografia ("{dados_usuario['biografia']}") e meu nicho ("{dados_usuario['nicho']}"), monte um dossiê de nível PhD:
                1. DETALHAMENTO DE POPULAÇÃO E ELEITORADO: Forneça as estimativas estatísticas detalhadas para {opcao_visualizacao}.
                2. TRÊS CENÁRIOS DE TOM DE DISCURSO DE GUERRA (Cenário A: Ruptura Crua, Cenário B: Contraponto Técnico de Dados, Cenário C: Apelo de Proteção Regional). Diga exatamente o gancho de abertura e a frase de impacto para cada tom.
                3. ANTÍDOTO DE REJEIÇÃO: O que o candidato jamais pode falar para o eleitorado dessa cidade específica.
                """
                try:
                    relatorio_bd = st.session_state['motor_ia'].generate_content(prompt_bd)
                    st.session_state[f'discurso_{opcao_visualizacao}'] = relatorio_bd.text
                except Exception as e:
                    st.error(f"Erro no motor de Big Data: {e}")
                    
        if f'discurso_{opcao_visualizacao}' in st.session_state:
            st.subheader(f"🔥 Diretrizes de Discurso e Estatísticas Adaptativas — {opcao_visualizacao}")
            st.markdown(st.session_state[f'discurso_{opcao_visualizacao}'])
            st.text_area("Copiar Dossiê Regional:", value=st.session_state[f'discurso_{opcao_visualizacao}'], height=120)

    # --- ABA 3: CONVERSÃO TERRITORIAL DE CAMPO ---
    with tab_conversao:
        st.header("🗺️ Plano de Infiltração Territorial")
        cidade_foco = st.selectbox("Selecione a praça para auditoria tática de cabos eleitorais:", options=dados_usuario['municipios'])
        
        st.subheader("🧮 Calculadora de Estrutura Terrestre (CRM)")
        col_crm1, col_crm2, col_crm3 = st.columns(3)
        with col_crm1:
            num_liderancas = st.number_input("Número de Generais de Base (Líderes) na Cidade", min_value=0, max_value=100, value=5, key=f"lid_{cidade_foco}")
        with col_crm2:
            media_votos_lider = st.number_input("Cobrança de Meta por General (Votos)", min_value=10, max_value=5000, value=1000, key=f"meta_{cidade_foco}")
        with col_crm3:
            votos_opiniao_insta = st.slider("Arrasto Projetado por Tráfego Pago (Aéreo)", min_value=0, max_value=20000, value=2000, key=f"traf_{cidade_foco}")
            
        votos_estrutura_total = num_liderancas * media_votos_lider
        votos_projetados_totais = votos_estrutura_total + votos_opiniao_insta
        
        st.metric("Projeção Real de Urna (Alvo Local)", f"{votos_projetados_totais:,} Votos")
        
        if st.button(f"🔥 Forjar Plano de Ocupação para {cidade_foco}"):
            with st.spinner("Forjando ordens de batalha para as lideranças..."):
                prompt_analise = f"""
                Gere um Relatório de Ocupação Territorial Estratégica para a cidade de {cidade_foco}.
                Meta Terrestre: {votos_estrutura_total} baseada em {num_liderancas} líderes de base.
                Meta Digital: {votos_opiniao_insta} votos de opinião.
                
                Com base na BIOGRAFIA do candidato, entregue uma resposta arrojada de guerrilha:
                1. COBRANÇA DE DESEMPENHO: Qual a estratégia institucional para amarrar e auditar esses {num_liderancas} líderes para que entreguem a meta sem trair o comitê?
                2. OPERAÇÃO DE ASSALTO: Qual ação de forte impacto de rua deve ser feita em {cidade_foco} para neutralizar os deputados tradicionais dominantes.
                """
                try:
                    relatorio_cidade = st.session_state['motor_ia'].generate_content(prompt_analise)
                    st.session_state[f'relatorio_{cidade_foco}'] = relatorio_cidade.text
                except Exception as e:
                    st.error(f"Erro no motor territorial: {e}")
                    
        if f'relatorio_{cidade_foco}' in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state[f'relatorio_{cidade_foco}'])
            st.text_area("Copiar Relatório Territorial:", value=st.session_state[f'relatorio_{cidade_foco}'], height=120)

    # --- ABA 4: ALOCAÇÃO E CONTROLE FINANCEIRO (DINÂMICO POR MUNICÍPIO SELECIONADO) ---
    with tab_financeiro:
        st.header("💰 Planejamento Financeiro de Mobilização e Pessoal")
        st.markdown("Controle orçamentário centralizado. As seções de custos abaixo são geradas **dinamicamente** com base nos municípios que você ativou no menu lateral.")
        
        lista_dados_financeiros = []
        
        # AJUSTE CHAVE: O laço agora lê e renderiza exatamente a lista dinâmica do usuário
        for municipio in dados_usuario['municipios']:
            st.markdown(f"#### ⚙️ Orçamento de Pessoal Terrestre — **{municipio}**")
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                militantes = st.number_input(f"Militantes / Equipe de Rua (Qtd)", min_value=0, value=10, key=f"mil_q_{municipio}")
                sal_militante = st.number_input(f"Custo por Militante (R$)", min_value=0, value=1500, key=f"mil_s_{municipio}")
            with col_f2:
                coordenadores = st.number_input(f"Coordenadores Locais (Qtd)", min_value=0, value=1, key=f"coord_q_{municipio}")
                sal_coordenador = st.number_input(f"Custo por Coordenador (R$)", min_value=0, value=3500, key=f"coord_s_{municipio}")
            with col_f3:
                fiscais = st.n                     
