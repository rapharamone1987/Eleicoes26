import os
from groq import Groq

def configurar_inteligencia(api_key, dados_candidato):
    """
    Inicializa o cliente do Groq e encapsula a engenharia de prompt
    de sistema com base no onboarding dinâmico e livre do candidato.
    """
    client = Groq(api_key=api_key)
    
    nome = dados_candidato.get('nome', 'Candidato')
    partido = dados_candidato.get('partido', 'Partido')
    idade = dados_candidato.get('idade', '40')
    nicho_livre = dados_candidato.get('nicho', 'Geral')
    
    lista_municipios = dados_candidato.get('municipios', [])
    municipios_texto = ", ".join(lista_municipios) if lista_municipios else "Todo o Rio Grande do Sul"

    prompt_sistema = f"""
    Você é o Estrategista-Chefe e Consultor de Marketing Político Sênior (nível PhD) da campanha de {nome} ({partido}).
    Cargo Pleiteado: Deputado Federal pelo Rio Grande do Sul (Eleições 2026).
    Perfil Demográfico: {idade} anos.
    
    [MATRIZ GEOPOLÍTICA E NARRATIVA]
    - Território de Operação (Cidades-Foco no RS): {municipios_texto}
    - Nicho Ideológico / Pauta Central de Ataque: {nicho_livre}
    
    [DIRETRIZES DO COMITÊ CENTRAL - OBRIGATÓRIO]
    1. TOM E POSTURA: Responda com pragmatismo, altivez e profundidade técnica. O eleitor gaúcho é altamente politizado. Evite clichês e discursos populistas genéricos. Ajuste o vocabulário para a realidade socioeconômica de {municipios_texto}.
    2. MICROSEGMENTAÇÃO: Sempre que gerar estratégias ou conteúdos, amarre a pauta de "{nicho_livre}" diretamente às características locais de {municipios_texto} (ex: infraestrutura, cooperativismo, segurança ou comércio local dessas áreas).
    3. TRAVA JURÍDICA DE COMPLIANCE (TSE): Você está terminantemente proibido de sugerir pedidos explícitos de voto (como "vote em mim", "conto com seu voto") para evitar processos por propaganda antecipada ou irregular. Use termos de posicionamento e construção de imagem ("Defendo que", "Nosso compromisso é", "Precisamos debater").
    4. ÉTICA DE CAMPANHA: Não invente fake news ou dados demográficos falsos. Se precisar citar cenários, baseie-se em dados lógicos e plausíveis de administração pública.
    """

    class GroqCampaignEngine:
        def __init__(self, groq_client, system_prompt):
            self.client = groq_client
            self.system_prompt = system_prompt
            self.model_name = "llama-3.1-70b-versatile" 

        def generate_content(self, prompt_usuario):
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt_usuario}
                ],
                temperature=0.3,
                max_tokens=2048
            )
            class ResponseObj:
                def __init__(self, text):
                    self.text = text
            return ResponseObj(completion.choices[0].message.content)

    return GroqCampaignEngine(client, prompt_sistema)
