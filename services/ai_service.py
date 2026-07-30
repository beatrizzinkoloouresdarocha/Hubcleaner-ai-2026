import os
import time
from google import genai

class AIService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)

    def analisar_contato_spam(self, email, nome=""):
        """Analisa cadastros para identificar spam ou testes."""
        prompt = (
            f"Analise o seguinte cadastro de CRM e determine se parece ser um teste, spam ou e-mail temporário falso.\n"
            f"Nome: {nome}\n"
            f"E-mail: {email}\n\n"
            f"Responda apenas com 'SPAM' se for falso/teste ou 'VALIDO' se parecer um usuário legítimo."
        )

        # Pausa necessária para respeitar o limite de 5 requisições/min no plano gratuito
        time.sleep(12)

        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
            )
            resultado = response.text.strip().upper()
            return "SPAM" in resultado
        except Exception as e:
            print(f"Erro na análise do Gemini: {e}")
            return False