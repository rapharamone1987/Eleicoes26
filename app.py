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
        "perfil_socioeconomico": "Capital do State. Predomínio do setor de serviços, funcionalismo público, comércio adensado e forte núcleo universitário. Alto IDH (0.805).",
        "comportamento_historico": "Eleitorado altamente fragmentado, crítico e polarizado. Divisão histórica acentuada entre periferias (voto de demanda estrutural) e bairros centrais (voto ideológico de opinião/redes).",
        "principais_dores": "Segurança nos eixos comerciais, revitalização do centro urbano, eficiência no transporte público e desburocratização tributária municipal."
    },
    "CAXIAS DO SUL": {
        "regiao": "Serra Gaúcha",
        "eleitorado_total": 348000,
        "abstencao_media": "18.1%",
        "perfil_socioeconomico": "Segundo maior polo econômico do estado. Forte DNA metal-mecânico, industrial, vitivinicultor e cooperativista. Baixo desemprego.",
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

# --- LISTA OFICIAL COMPLETA DOS 497 MUNICÍPIOS DO RIO GRANDE DO SUL ---
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
# 4. PAINEL DE CONTROLE LATERAL (TELA COMERCIAL COM FILTRO DE BUSCA)
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
    
    st.markdown("---")
    st.markdown("**📍 Seleção Avançada de Cidades**")
    # EXIGÊNCIA RESOLVIDA: Adicionado campo de texto focado no tablet para buscar e filtrar municípios
    busca_municipio = st.text_input("🔎 Digite para buscar na lista de 497 cidades do RS:", value="", placeholder="Ex: Osorio / Tramandai / Porto")
    
    # Filtração imediata na memória do script baseado na digitação do usuário
    if busca_municipio:
        lista_filtrada = [cidade for cidade in MUNICICIPIOS_497_RS if busca_municipio.upper() in cidade]
        if not lista_filtrada:
            st.sidebar.warning("Nenhum município localizado com esse nome.")
            lista_filtrada = MUNICICIPIOS_497_RS
    else:
        lista_filtrada = MUNICICIPIOS_497_RS

    municipios_alvo = st.multiselect(
        "Selecione os Municípios Alvo da Lista:", 
        options=lista_filtrada,
        default=[] 
    )
    
    st.caption("Dica: se a cidade sumiu da rolagem, use o campo de busca acima para filtrá-la na tela.")
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

    # --- ABA 2: BIG DATA GEOPOLÍTICO REATIVO POR ALVO (RESOLVIDO) ---
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
            st.warning(f"🌐 Varredura Ativa: O município '{opcao_visualizacao}' exige estatísticas dinâmicas via IA.")
            st.markdown("*O motor vai extrair do seu ecossistema as estim
