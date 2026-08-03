import os
from google import genai

class AIService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ ATENÇÃO: GEMINI_API_KEY não foi encontrada no .env!")
        self.client = genai.Client(api_key=api_key)

    def analisar_contato(self, contato):
        """
        Recebe o objeto ou dicionário do contato e retorna a decisão da IA.
        """
        try:
            # Tratamento para aceitar tanto dicionário quanto objeto SimplePublicObjectWithAssociations
            if isinstance(contato, dict):
                props = contato.get('properties', contato)
            else:
                props = getattr(contato, 'properties', {}) or {}

            # Extrai os dados das propriedades do HubSpot com fallback seguro
            email = props.get('email', '') if isinstance(props, dict) else getattr(props, 'email', '')
            firstname = props.get('firstname', '') if isinstance(props, dict) else getattr(props, 'firstname', '')
            lastname = props.get('lastname', '') if isinstance(props, dict) else getattr(props, 'lastname', '')

            nome = f"{firstname} {lastname}".strip()

            prompt = f"""
            Analise as informações do seguinte contato do CRM HubSpot para identificar se é um lead inválido, spam ou de teste:
            - Nome: {nome}
            - E-mail: {email}
            
            Responda em formato JSON simples:
            {{
                "valido": true/false,
                "motivo": "Explicação breve"
            }}
            """

            resposta = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return resposta.text
        except Exception as e:
            print(f"❌ Erro ao analisar contato com Gemini: {e}")
            return None