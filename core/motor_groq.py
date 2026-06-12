from groq import Groq


def configurar_inteligencia(api_key: str, dados_candidato: dict):
    """
    Configura o cliente Groq com os dados do candidato.
    
    Args:
        api_key: Chave de API do Groq
        dados_candidato: Dicionário com dados do candidato (nome, idade, partido, nicho, regioes)
    
    Returns:
        Cliente Groq configurado
    """
    client = Groq(api_key=api_key)
    
    # Armazena dados do candidato no cliente para contexto
    client.dados_candidato = dados_candidato
    client.context_sistema = _gerar_contexto_sistema(dados_candidato)
    
    return client


def _gerar_contexto_sistema(dados_candidato: dict) -> str:
    """
    Gera o prompt de contexto do sistema baseado no perfil do candidato.
    """
    return f"""Você é um especialista em estratégia eleitoral e marketing político de alta performance.
    
Você está trabalhando com o candidato: {dados_candidato['nome']}
- Idade: {dados_candidato['idade']} anos
- Partido/Federação: {dados_candidato['partido']}
- Nicho/Pauta Central: {dados_candidato['nicho']}
- Regiões Prioritárias: {', '.join(dados_candidato['regioes'])}

Sua missão é gerar análises estratégicas, mapas de votação, e conteúdos criativos alinhados com este perfil.
Mantenha o tom profissional, dados-driven, e focado em resultados eleitorais."""


class MotorGroq:
    """
    Wrapper para facilitar a integração com Streamlit.
    """
    def __init__(self, client: Groq, sistema_context: str):
        self.client = client
        self.sistema_context = sistema_context
    
    def generate_content(self, prompt: str, model: str = "mixtral-8x7b-32768") -> dict:
        """
        Gera conteúdo usando o Groq.
        
        Args:
            prompt: Prompt do usuário
            model: Modelo do Groq a utilizar
        
        Returns:
            Resposta com atributo .text para compatibilidade com Gemini
        """
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": self.sistema_context
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2048
        )
        
        # Wrapper para compatibilidade com interface do Gemini
        class ResponseWrapper:
            def __init__(self, content):
                self.text = content
        
        return ResponseWrapper(response.choices[0].message.content)
