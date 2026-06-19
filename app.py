import sys
import os
import streamlit as st
from groq import Groq

# ------------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA INTERFACE E AMBIENTE (TELA NEUTRA COMERCIAL)
# ------------------------------------------------------------------------------
st.set_page_config(page_title="Aegis Eleitoral PRO", layout="wide")

st.title("🛡️ Aegis Eleitoral — Inteligência de Guerrilha")
st.caption("Plataforma Avançada de Sala de Situação, Modelagem Neurolinguística (PNL) e Big Data — Eleições 2026")

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
        "comportamento_historico": "Eleitorado altamente fragmentado, crítico e polarizado. Divisão acentuada entre periferias e bairros centrais.",
        "principais_dores": "Segurança nos eixos comerciais, revitalização do centro urbano, eficiência no transporte público e desburocratização tributária municipal."
    },
    "CAXIAS DO SUL": {
        "regiao": "Serra Gaúcha",
        "eleitorado_total": 348000,
        "abstencao_media": "18.1%",
        "perfil_socioeconomico": "Segundo maior polo econômico do estado. Forte DNA metal-mecânico, industrial, vitivinicultor e cooperativista. Baixo desemprego.",
        "comportamento_historico": "Eleitorado de perfil conservador, pragmático e focado em pautas econômicas de livre mercado, ordem pública e valorização do trabalho.",
        "principais_dores": "Gargalos logísticos de escoamento (estradas federais), segurança nas zonas industriais e demandas por saúde suplementar."
    },
    "PASSO FUNDO": {
        "regiao": "Planalto Médio",
        "eleitorado_total": 152000,
        "abstencao_media": "16.5%",
        "perfil_socioeconomico": "Polo de saúde, educação superior e entroncamento logístico do agronegócio de alta precisão. Renda impulsionada pelas safras de grãos.",
        "comportamento_historico": "Voto tradicionalmente ligado a grandes lideranças locais. Forte influência do setor produtivo e sindicatos rurais.",
        "principais_dores": "Insegurança e roubo de defensivos em propriedades rurais, infraestrutura de rodovias estaduais secundárias e retenção de talentos técnicos."
    },
    "URUGUAIANA": {
        "regiao": "Fronteira Oeste",
        "eleitorado_total": 88000,
        "abstencao_media": "24.2%",
        "perfil_socioeconomico": "Maior porto seco da América Latina. Economia baseada na logística internacional do Mercosul, pecuária extensiva e grande lavoura arrozeira.",
        "comportamento_historico": "Eleitorado com alto índice de abstenção. Voto dependente de estruturas políticas consolidadas e forte apelo a demandas de segurança nacional.",
        "principais_dores": "Falta de policiamento nas rotas de fronteira, burocracia aduaneira sufocante e isolamento político em relação à capital."
    }
}

DADOS_ESTADUAIS_GERAIS = {
    "regiao": "Todo o Rio Grande do Sul",
    "eleitorado_total": 8600000,
    "abstencao_media": "19.8%",
    "perfil_socioeconomico": "Estado com forte equilíbrio entre o PIB industrial (Serra/Metropolitana) e a força do Agronegócio (Norte/Fronteira/Sul). Elevado índice de politização e IDH médio alto.",
    "comportamento_historico": "Tendência histórica a eleições plebiscitárias e polarizadas. Forte tradição de voto regionalizado.",
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
    "FREDERICO WESTPHALEN", "SANTO ÂNGELO", "ROSÁRIO DO SUL", "ITAQUI", "QUARAÍ", "JAGUARÃO", "ACEGUÁ", "AGUDO", 
    "ALMIRANTE TAMANDARÉ DO SUL", "ALPETRE", "ALTO ALEGRE", "ALTO FELIZ", "AMARAL FERRADOR", "AMETISTA DO SUL", 
    "ANDRÉ DA ROCHA", "ANTA GORDA", "ANTÔNIO PRADO", "ARAMBARÉ", "ARARICÁ", "ARATIBA", "ARROIO DO MEIO", 
    "ARROIO DO PADRE", "ARROIO DO TIGRE", "ARROIO DOS RATOS", "ÁRVOREZINHA", "AUGUSTO PESTANA", "AUREA", "BARÃO", 
    "BARÃO DE COTEGIPE", "BARÃO DO TRIUNFO", "BARRA DO GUARITA", "BARRA DO RIBEIRO", "BARRA DO RIO AZUL", 
    "BARRA DO QUARAÍ", "BARRA FUNDA", "BARRACÃO", "BARROS CASAL", "BENJAMIN CONSTANT DO SUL", "BOA VISTA DO BURICÁ", 
    "BOA VISTA DO CADEADO", "BOA VISTA DO INCRA", "BOA VISTA DO SUL", "BOM JESUS", "BOM PRINCÍPIO", "BOM RETIRO DO SUL", 
    "BOQUEIRÃO DO LEÃO", "BOSSOROCA", "BOZANO", "BRAGA", "BROCHIER", "BUTIÁ", "CAÇADOR", "CACHOEIRA DO SUL", 
    "CACIQUE DOBLE", "CAIBATÉ", "CAIÇARA", "CAMAQUÃ", "CAMARGO", "CAMBÁRA DO SUL", "CAMPESTRE DA SERRA", 
    "CAMPINA DAS MISSÕES", "CAMPINAS DO SUL", "CAMPO NOVO", "CAMPOS BORGES", "CANDELÁRIA", "CÂNDIDO GODÓI", 
    "CANDIOTA", "CANUDOS DO VALE", "CAPÃO DO CIPÓ", "CAPÃO DO LEÃO", "CAPELA DE SANTANA", "CAPITÃO", 
    "CAPIVARI DO SUL", "CARAÁ", "CASCA", "CASEIROS", "CATUÍPE", "CAVIANA", "CENTENÁRIO", "CERRITO", 
    "CERRO GRANDE", "CERRO GRANDE DO SUL", "CERRO LARGO", "CHAPADA", "CHARQUEADAS", "CHARRUA", "CHIAPETTA", 
    "CHUÍ", "CHUVISCA", "COLINAS", "COLORADO", "CONDOR", "CONSTANTINA", "COQUEIRO BAIXO", "COQUEIROS DO SUL", 
    "CORONEL BARROS", "CORONEL BICACO", "CORONEL PILAR", "COTRIGUAÇU", "COXILHA", "CRISSÍUMAL", "CRISTAL", 
    "CRISTAL DO SUL", "CRUZEIRO DO SUL", "DAVID CANABARRO", "DERRUBADAS", "DEZESSEIS DE NOVEMBRO", 
    "DILERMANDO DE AGUIAR", "DOIS LAJEADOS", "DOIS IRMÃOS", "DOIS IRMÃOS DAS MISSÕES", "DOUTOR MAURÍCIO CARDOSO", 
    "DOUTOR RICARDO", "ELDORADO DO SUL", "ENCANTADO", "ENCRUZILHADA DO SUL", "ENGENHO VELHO", "ENTRE-IJUÍS", 
    "ENTRE RIOS DO SUL", "ERIVAL SECO", "ERNESTINA", "ERVAL GRANDE", "ERVAL SECO", "ESMERALDA", "ESPERANÇA DO SUL", 
    "ESPUMOSO", "ESTAÇÃO", "ESTRELA VELHA", "EUGÊNIO DE CASTRO", "FAGUNDES VARELA", "FAXINAL DO SATURNO", 
    "FAXINALZINHO", "FAZENDA VILANOVA", "FELIZ", "FLORES DA CUNHA", "FLORIANO PEIXOTO", "FONTURA XAVIER", 
    "FORMIGUEIRO", "FORQUETINHA", "FORQUILHA", "GARRUCHOS", "GAURAMA", "GENERAL CÂMARA", "GENTIL", "GETÚLIO VARGAS", 
    "GIRUÁ", "GLORINHA", "GRAMADO DOS LOUREIROS", "GRAMADO XAVIER", "GUABIJU", "GUAPORÉ", "GUARANI DAS MISSÕES", 
    "HARMONIA", "HERVAL", "HERVEIRAS", "HORIZONTINA", "HULHA NEGRA", "HUMAITÁ", "IBARAMA", "IBIASSUCE", 
    "IBIRAIARAS", "IBIRAPUITÃ", "IBIRUBÁ", "IGREJINHA", "ILÓPOLIS", "IMIGRANTE", "INHACORÁ", "IPÊ", 
    "IPIRANGA DO SUL", "IRAI", "ITAARA", "ITACURUBI", "ITAPUCA", "ITATI", "IVOTI", "JABOTICABA", "JACUTINGA", 
    "JAGUARI", "JAQUIRANA", "JARI", "JÓIA", "JÚLIO DE CASTILHOS", "LAGOÃO", "LAGOA DOS TRÊS CANTOS", 
    "LAGOA VERMELHA", "LAGOA BONITA DO SUL", "LIBERATO SALZANO", "MAÇAMBARÁ", "MACHADINHO", "MAMPITUBA", 
    "MANOEL VIANA", "MAQUINÉ", "MARATÁ", "MARCELINO RAMOS", "MARIANA PIMENTEL", "MARIANO MORO", "MARQUÊS DE SOUZA", 
    "MATA", "MATO CASTELHANO", "MATO LEITÃO", "MATO QUEIMADO", "MAXIMILIANO DE ALMEIDA", "MINAS DO LEÃO", 
    "MIRAGUAI", "MONTAURI", "MONTE ALEGRE DOS CAMPOS", "MONTE BELO DO SUL", "MORRINHOS DO SUL", "MORRO REUTER", 
    "MORRO REDONDO", "MUITOS CAPÕES", "MULITERNO", "NÃO-ME-TOQUE", "NICOLAU VERGUEIRO", "NÔNOAI", "NOVA ALVORADA", 
    "NOVA ARAÇÁ", "NOVA BASSANO", "NOVA BRÉSCIA", "NOVA CANDELÁRIA", "NOVA ESPERANÇA DO SUL", "NOVA HARTZ", 
    "NOVA PÁDUA", "NOVA PALMA", "NOVA PETRÓPOLIS", "NOVA PRATA", "NOVA RAMADA", "NOVA ROMA DO SUL", "NOVA SANTA RITA", 
    "NOVO BARREIRO", "NOVO CABRAIS", "NOVO MACHADO", "NOVO TIRADENTES", "NOVO XINGU", "PAIAL", "PALMARES DO SUL", 
    "PALMITINHO", "PARAÍ", "PARAÍSO DO SUL", "PARECI NOVO", "PAROBÉ", "PASSA SETE", "PASSO DO SOBRADO", 
    "PAULO BENTO", "PEDRAS ALTAS", "PEDRO OSÓRIO", "PEJUÇARA", "PINHAL", "PINHAL DA SERRA", "PINHAL GRANDE", 
    "PINHEIRINHO DO VALE", "PINHEIRO MACHADO", "PINTO BANDEIRA", "PIRATINI", "PLANALTO", "POÇO DAS ANTAS", 
    "PONTÃO", "PONTE PRETA", "PORTO LUCENA", "PORTO MAUÁ", "PORTO XAVIER", "POUSO NOVO", "PRESIDENTE LUCENA", 
    "PROGRESSO", "PROTÁSIO ALVES", "PUTINGA", "QUATRO IRMÃOS", "QUEVEDOS", "REDENTORA", "RELVADO", "RESTINGA SECA", 
    "RIO DOS ÍNDIOS", "RIO PARARDO", "RIOZINHO", "ROCA SALES", "ROQUE GONZALES", "RONDA ALTA", "RONDINHA", 
    "ROLANDO", "SALDANHA MARINHO", "SALTO DO JACUÍ", "SALVADOR DO SUL", "SANANDUVA", "SANTA CLARA DO SUL", 
    "SANTA MARGARIDA DO SUL", "SANTA MARIA DO HERVAL", "SANTANA DA BOA VISTA", "SANTIAGO DO SUL", 
    "SANTO ANTÔNIO DO PALMA", "SANTO ANTÔNIO DO PLANALTO", "SANTO AUGUSTO", "SANTO CRISTO", "SÃO PEDRO DO SUL", 
    "SÃO SEBASTIÃO DO CAÍ", "SÃO VALENTIM", "SÃO VALENTIM DO SUL", "SÃO VENDELINO", "SÃO VICENTE DO SUL", 
    "SÉRIO", "SERTÃO", "SERTÃO SANTANA", "SETE DE SETEMBRO", "SEVERIANO DE ALMEIDA", "SILVEIRA MARTINS", 
    "SINIMBU", "SOBRADINHO", "TAPEJARA", "TAPERA", "TAPES", "TAQUARI", "TAQUARUÇU DO SUL", "TEUTÔNIA", 
    "TIO HUGO", "TIRADENTES DO SUL", "TOROPI", "TRAVESSEIRO", "TRÊS CACHOEIRAS", "TRÊS COROAS", "TRÊS DE MAIO", 
    "TRÊS FORQUILHAS", "TRÊS PALMEIRAS", "TRÊS PASSOS", "TRINDADE DO SUL", "TRIUNFO", "TUCUNDUVA", "TUNAS", 
    "TUPANCIRETÃ", "TUPANDI", "TUPARENDI", "TURUÇU", "UNISTALDA", "VALE REAL", "VALE DO SOL", "VALE VERDE", 
    "VANINI", "VERANÓPOLIS", "VESPASIANO CORRÊA", "VIADUTOS", "VICENTE DUTRA", "VICTOR GRAEFF", "VILA FLORES", 
    "VILA LÂNGARO", "VILA MARIA", "VILA NOVA DO SUL", "VISTA ALEGRE", "VISTA ALEGRE DO PRATA", "VISTA GAÚCHA", 
    "VITÓRIA DAS MISSÕES", "WESTFÁLIA"
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

    prompt_sistema = f"""
    Você é o Estrategista-Chefe, General de Sala de Crise e PhD em Ciência Política e Sociologia da campanha de {nome} ({partido}), disputando a eleição de Deputado Federal pelo Rio Grande do Sul.
    Idade: {idade} anos.
    
    [PRONTUÁRIO BIOGRÁFICO REAL DO CANDIDATO]
    {biografia}
    
    [TRINCHEIRA TEMÁTICA CENTRAL]
    {nicho_livre}
    
    [DIRETRIZES DE GUERRA DO COMITÊ CENTRAL - IMPRESCINDÍVEL]
    1. TOM E POSTURA: Responda com absoluto pragmatismo, agressividade mercadológica e rigor sociológico. Ignore conselhos pacifistas ou cartilhas corporativas confortáveis.
    2. ENGENHARIA DE DISCURSO E PNL: Quando solicitado a gerar conteúdos ou analisar personas, aplique com precisão cirúrgica os metamodelos de linguagem da Programação Neurolinguística (Visual, Auditivo, Cinestésico) e use gatilhos mentais avançados de assalto psicológico (Autoridade, Escassez, Conectividade Regional).
    3. COMPLIANCE JURÍDICO TSE: Comande narrativas avassaladoras e mobilizadoras, mas NUNCA use termos de pedido explícito de voto (como "vote em mim", "conto com seu voto", "me eleja") para blindar a chapa contra processos legais de propaganda antecipada. Use termos institucionais de alta voltagem ("Defendo intransigentemente que", "Temos o dever de confrontar").
    """

    class EngineGuerrilha:
        def generate_content(self, prompt_usuario):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": prompt_usuario}
                ],
                temperature=0.1,  # Máxima precisão lógica e sem alucinações
                max_tokens=2500
            )
            class Wrapper:
                def __init__(self, text): self.text = text
            return Wrapper(completion.choices[0].message.content)
            
    return EngineGuerrilha()

# ------------------------------------------------------------------------------
# 4. PAINEL DE CONTROLE LATERAL (TELA COMERCIAL TOTALMENTE NEUTRA)
# ------------------------------------------------------------------------------
st.sidebar.title("👤 Inteligência de Origem")
st.sidebar.markdown("*Insira o DNA político do candidato para alimentar o ecossistema.*")

with st.sidebar.form("contexto_campanha"):
    nome_input = st.text_input("Nome de Urna", placeholder="Ex: Capitão Veríssimo")
    idade_input = st.number_input("Idade", min_value=18, max_value=90, value=35)
    partido_input = st.text_input("Partido / Federação", placeholder="Ex: NOVO / PP / MDB")
    nicho_input = st.text_input("Trincheira / Pauta Central", placeholder="Ex: Defesa do Livre Mercado / Segurança Pública")
    
    biografia_input = st.text_area(
        "Biografia e Capital Político do Candidato", 
        placeholder="Ex: Detalhe o recall político, profissão real, histórico com as bases de veteranos ou produtores rurais..."
    )
    
    # EXIGÊNCIA RESOLVIDA: O botão apenas valida os dados de cadastro biográfico geral
    ativar_motor = st.form_submit_button("🔥 Inicializar Motor Cognitivo")

# ------------------------------------------------------------------------------
# 5. INICIALIZAÇÃO DA SESSÃO NEURAL
# ------------------------------------------------------------------------------
if ativar_motor:
    if not nome_input or not partido_input or not nicho_input or not biografia_input:
        st.sidebar.error("⚠️ Erro Estratégico: Preencha todos os campos biográficos para calibrar o motor de PNL.")
    else:
        dados_candidato = {
            "nome": nome_input, 
            "idade": idade_input, 
            "partido": partido_input, 
            "nicho": nicho_input, 
            "biografia": biografia_input
        }
        st.session_state['dados_candidato'] = dados_candidato
        st.session_state['motor_ia'] = colocar_motor_no_ar = baixar_motor = ativar_motor_campanha(api_key, dados_candidato)
        
        for modulo in ["swot", "bigdata", "personas", "criativo"]:
            st.session_state[f"chat_{modulo}"] = []
        st.toast("Motor Cognitivo Ativo com Sucesso!", icon="✅")

# ------------------------------------------------------------------------------
# 6. CÉLULA DE INTERAÇÃO DIALÓGICA (DEBATE COM O PHD)
# ------------------------------------------------------------------------------
def renderizar_bunker_discussao(modulo_key, contexto_analise):
    st.markdown("---")
    st.subheader("💬 Bunker de Discussão Tática com o PhD")
    st.caption("Conteste as análises acima, simule ataques de adversários ou peça roteiros de reação imediata.")
    
    if f"chat_{modulo_key}" not in st.session_state:
        st.session_state[f"chat_{modulo_key}"] = []
        
    for msg in st.session_state[f"chat_{modulo_key}"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt_chat := st.chat_input("Digite sua ordem ou contra-argumento estratégico:", key=f"input_{modulo_key}"):
        with st.chat_message("user"):
            st.markdown(prompt_chat)
        st.session_state[f"chat_{modulo_key}"].append({"role": "user", "content": prompt_chat})
        
        with st.spinner("O PhD está redesenhando as linhas de combate..."):
            prompt_consolidado = f"""
            [CONTEXTO DO RELATÓRIO DO MÓDULO]
            {contexto_analise}
            
            [HISTÓRICO DO DEBATE DA SALA DE SITUAÇÃO]
            {st.session_state[f'chat_{modulo_key}']}
            
            [NOVA DIRETRIZ OU QUESTIONAMENTO DO COMITÊ CENTRAL]
            {prompt_chat}
            
            Entregue uma resposta ultra-arrojada, cirúrgica e de aplicação imediata na rua. Mantenha os guardrails do TSE.
            """
            try:
                resposta_chat = st.session_state['motor_ia'].generate_content(prompt_consolidado)
                with st.chat_message("assistant"):
                    st.markdown(resposta_chat.text)
                st.session_state[f"chat_{modulo_key}"].append({"role": "assistant", "content": resposta_chat.text})
                st.rerun()
            except Exception as e:
                st.error(f"Erro na comunicação tática: {e}")

# ------------------------------------------------------------------------------
# 7. MAPA OPERACIONAL DE ABAS (INTERFACES 100% INDEPENDENTES POR COMPONENTE)
# ------------------------------------------------------------------------------
tab_diagnostico, tab_bigdata, tab_personas, tab_criativo = st.tabs([
    "🧠 Diagnóstico SWOT de Ruptura", 
    "📊 Big Data Geopolítico",
    "👥 Modelagem de Eletropersonas (PNL)", 
    "📝 Fábrica de Conteúdo de Guerrilha"
])

if 'motor_ia' in st.session_state:
    dados_usuario = st.session_state['dados_candidato']
    
    # --- ABA 1: PLANO DE RUPTURA INTERREGIONAL ---
    with tab_diagnostico:
        st.header("🧠 Análise SWOT de Assalto Territorial")
        st.markdown("Mapeamento crú de vulnerabilidades das dinastias políticas locais contra seu capital político.")
        
        # EXIGÊNCIA RESOLVIDA: Seleção independente e intuitiva com busca nativa por teclado no tablet
        cidade_swot = st.selectbox("Selecione a praça de guerra para auditoria SWOT:", options=MUNICICIPIOS_497_RS, key="swot_cidade_indep")
        
        if st.button(f"🔥 Forjar Plano de Ruptura para {cidade_swot}"):
            with st.spinner("Desmontando defesas adversárias..."):
                prompt_swot = f"Gere um Diagnóstico de Ruptura Eleitoral para a cidade de {cidade_swot}. Faça uma análise SWOT agressiva e profunda que confronte diretamente minha biografia contra as vulnerabilidades políticas locais."
                try:
                    res_swot = st.session_state['motor_ia'].generate_content(prompt_swot)
                    st.session_state[f'swot_rel_{cidade_swot}'] = res_swot.text
                except Exception as e:
                    st.error(f"Erro no motor: {e}")
                    
        if f'swot_rel_{cidade_swot}' in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state[f'swot_rel_{cidade_swot}'])
            st.text_area("Copiar SWOT:", value=st.session_state[f'swot_rel_{cidade_swot}'], height=100)
            renderizar_bunker_discussao("swot", st.session_state[f'swot_rel_{cidade_swot}'])

    # --- ABA 2: BIG DATA GEOPOLÍTICO REATIVO ---
    with tab_bigdata:
        st.header("📊 Inteligência Estatística de Dados Demográficos")
        
        # EXIGÊNCIA RESOLVIDA: Seleção independente e intuitiva com busca nativa
        cidade_bd = st.selectbox("Selecione o município alvo para extração de Big Data:", options=["Consolidado Estadual (Geral)"] + MUNICICIPIOS_497_RS, key="bd_cidade_indep")
        
        if cidade_bd in DADOS_GEOPOLITICOS_RS:
            bd = DADOS_GEOPOLITICOS_RS[cidade_bd]
            modo_ia = False
        elif id_est := cidade_bd == "Consolidado Estadual (Geral)":
            bd = DADOS_ESTADUAIS_GERAIS
            modo_ia = False
        else:
            modo_ia = True
            
        if not modo_ia:
            col_b1, col_b2, col_b3 = st.columns(3)
            col_b1.metric("Eleitorado Alvo Fixo", f"{bd['eleitorado_total']:,} Votos")
            col_b2.metric("Abstenção Média Histórica", bd['abstencao_media'])
            col_b3.metric("Recorte Geográfico", bd['regiao'])
            
            col_i1, col_i2 = st.columns(2)
            with col_i1: st.info(f"**Matriz Socioeconômica:**\n\n{bd['perfil_socioeconomico']}")
            with col_i2: st.warning(f"**Comportamento de Urna Histórico:**\n\n{bd['comportamento_historico']}")
            contexto_bd = str(bd)
        else:
            st.warning(f"🌐 Varredura Ativa: O município '{cidade_bd}' exige processamento dinâmico da IA.")
            contexto_bd = f"Município dinâmico fora da âncora: {cidade_bd}"
            
        if st.button(f"🧠 Puxar Dossiê de Inteligência e Discurso para {cidade_bd}"):
            with st.spinner(f"Varrendo registros de população e comportamento de {cidade_bd}..."):
                prompt_bd = f"Gere dados detalhados de população estimada, eleitorado aproximado, abstenção média histórica e a matriz econômica real da cidade de {cidade_bd}, Rio Grande do Sul. Monte 3 cenários arrojados de tom de voz para submeter esse eleitorado."
                try:
                    res_bd = st.session_state['motor_ia'].generate_content(prompt_bd)
                    st.session_state[f'bd_rel_{cidade_bd}'] = res_bd.text
                except Exception as e:
                    st.error(f"Erro: {e}")
                    
        if f'bd_rel_{cidade_bd}' in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state[f'bd_rel_{cidade_bd}'])
            st.text_area("Copiar Big Data:", value=st.session_state[f'bd_rel_{cidade_bd}'], height=100)
            contexto_bd += "\n" + st.session_state[f'bd_rel_{cidade_bd}']
            
        renderizar_bunker_discussao("bigdata", contexto_bd)

    # --- ABA 3: MODELAGEM DE ELETROPERSONAS (NOVA REQUISIÇÃO JÁ INTEGRADA) ---
    with tab_personas:
        st.header("👥 Modelagem Psicológica e Mapeamento de Eletropersonas")
        st.markdown("Projete os arquétipos e perfis neuro-sociológicos dominantes do território para calibrar seus gatilhos de PNL.")
        
        # EXIGÊNCIA RESOLVIDA: Seleção territorial totalmente independente e intuitiva
        cidade_personas = st.selectbox("Selecione o município para mapear as personas alvo:", options=MUNICICIPIOS_497_RS, key="personas_cidade_indep")
        
        if st.button(f"👥 Forjar Matriz de 3 Personas Alvo para {cidade_personas}"):
            with st.spinner(f"Mapeando o subconsciente do eleitorado de {cidade_personas}..."):
                prompt_personas = f"""
                Estude o perfil sociopolítico da cidade de {cidade_personas}.
                Com base na minha biografia ("{dados_usuario['biografia']}"), monte um dossiê sociológico estruturado gerando exatamente **3 Eletropersonas Principais e Dominantes** da cidade.
                
                Para CADA UMA das 3 personas, entregue obrigatoriamente em tópicos rígidos:
                1. PERFIL DO ALVO: Nome do arquétipo, idade média, faixa de renda e ocupação típica na cidade.
                2. SISTEMA VACILANTE (PNL): Identifique se a persona é predominantemente VISUAL (responde a imagens/estética), AUDITIVA (responde a dados, tom e falas estruturadas) ou CINESTÉSICA (responde a sentimento, aperto de mão, senso de proteção).
                3. GATILHO MENTAL DE ASSALTO: Qual gatilho psicológico perfura a defesa desse indivíduo (Autoridade, Escassez, Urgência Regional, Prova Social).
                4. A OBJEÇÃO SECRETA: O medo ou preconceito inconsciente que faz essa persona rejeitar um candidato com o meu perfil.
                5. ANTÍDOTO DE PNL (A FRASSE DE IMPACTO): Escreva, entre aspas, a frase exata de posicionamento institucional que eu devo verbalizar na feira, no rádio ou no Reels que destrói a objeção dessa persona e desarma sua resistência de forma imediata (respeitando o compliance de nunca pedir voto).
                """
                try:
                    res_personas = st.session_state['motor_ia'].generate_content(prompt_personas)
                    st.session_state[f'personas_rel_{cidade_personas}'] = res_personas.text
                except Exception as e:
                    st.error(f"Erro no motor de PNL: {e}")
                    
        if f'personas_rel_{cidade_personas}' in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state[f'personas_rel_{cidade_personas}'])
            st.text_area("Copiar Painel de Personas:", value=st.session_state[f'personas_rel_{cidade_personas}'], height=100)
            renderizar_bunker_discussao("personas", st.session_state[f'personas_rel_{cidade_personas}'])

    # --- ABA 4: FÁBRICA DE POSTS DIALÓGICA ---
    with tab_criativo:
        st.header("📝 Fábrica de Comunicação e Conteúdo de Guerrilha")
        st.markdown("Gere linhas editoriais imunes a processos judiciais do TSE, contextualizadas ao território.")
        
        # EXIGÊNCIA RESOLVIDA: Seleção independente e intuitiva
        cidade_criativo = st.selectbox("Afunilar alvo narrativo para qual cidade?", options=["Foco Geral do Estado"] + MUNICICIPIOS_497_RS, key="criativo_cidade_indep")
        
        canal = st.selectbox("Formato da Arma Digital", ["Roteiro de Vídeo Curto (Reels Agressivo)", "Carrossel de Confronto Sociológico", "Nota de Ataque Institucional"])
        
        # EXIGÊNCIA RESOLVIDA: O campo de notícia do dia tornou-se opcional para permitir geração livre perpétua
        pauta_dia = st.text_area(
            "O Fato Político ou Dor do Dia (OPCIONAL):", 
            placeholder="Deixe em branco para gerar uma Linha Editorial Perpétua de Posicionamento baseada puramente na dor histórica da cidade e na sua biografia..."
        )
        
        if st.button("🚀 Disparar Linha de Produção Digital"):
            with st.spinner("Redigindo peça de alta voltagem sob as travas do TSE..."):
                if pauta_dia:
                    diretriz_conteudo = f"Fato político ou notícia do dia para exploração imediata: '{pauta_dia}'."
                else:
                    diretriz_conteudo = "Nenhum fato específico fornecido. Puxe a linha histórica de dores econômicas da cidade e monte uma Linha Editorial Perpétua de Posicionamento focado em quebrar o status quo."
                    
                prompt_criativo = f"""
                Gere uma peça de comunicação política crua e mobilizadora no formato [{canal}] focado na praça [{cidade_criativo}].
                Contexto de pauta: {diretriz_conteudo}
                
                ESTRUTURA DA RESPOSTA:
                1. HOOK / O GANCHO DE PNL (Primeiros 3 segundos focados no canal sensorial dominante para travar o dedo no feed).
                2. ARGUMENTO DE GUERRA (Exponha a dor ou a linha editorial histórica, injete a biografia do candidato como ponto de autoridade institucional).
                3. CHAMADA INSTITUCIONAL (Engajamento e convocação de debate, sem qualquer pedido explícito de voto).
                """
                try:
                    peca_final = st.session_state['motor_ia'].generate_content(prompt_criativo)
                    st.session_state['peca_comunicacao_atual'] = peca_final.text
                except Exception as e:
                    st.error(f"Erro na fábrica de criativos: {e}")
                    
        if 'peca_comunicacao_atual' in st.session_state:
            st.markdown("---")
            st.subheader("🔥 Peça Pronta para Distribuição")
            st.markdown(st.session_state['peca_comunicacao_atual'])
            st.text_area("Copiar Peça para WhatsApp/Social:", value=st.session_state['peca_comunicacao_atual'], height=100)
            renderizar_bunker_discussao("criativo", st.session_state['peca_comunicacao_atual'])

else:
    with tab_diagnostico:
        st.info("👋 Central Aegis Eleitoral Zerada e Pronta para Onboarding. Insira os dados do perfil e a biografia profunda do candidato na barra lateral para abrir a sala de situação.")
