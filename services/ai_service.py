import os
import time
from google import genai

class AIService:
    def __init__(self):
        self.client = genai.Client()

    def analisar_contato(self, contato):
        prompt = f"""
        Analise o seguinte contato do CRM e determine se o e-mail ou dados parecem ser um teste, inválidos ou spam:
        - Nome: {contato.get('firstname', '')} {contato.get('lastname', '')}
        - Email: {contato.get('email', '')}

        Responda apenas com:
        - 'MANTER' se o contato parecer legítimo.
        - 'REMOVER' se for spam, teste ou e-mail inválido.
        """

        try:
            time.sleep(4)  # Pausa de 4 segundos para evitar limite de requisições por minuto
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            print(f"Erro na análise do Gemini: {e}")
            return "ERRO"