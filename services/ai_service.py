import os
from google import genai

class AIService:
    def __init__(self):
        # Inicializa o cliente oficial da biblioteca 'google-genai'
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ ATENÇÃO: GEMINI_API_KEY não foi encontrada no arquivo .env!")
        self.client = genai.Client(api_key=api_key)

    def analisar_contato(self, contato_info):
        """
        Analisa as informações do contato e determina se deve ser REMOVIDO ou MANTIDO.
        Aceita tanto uma string formatada quanto um dicionário com os dados do contato.
        """
        # Se for passado um dicionário, converte em uma string descritiva
        if isinstance(contato_info, dict):
            email = contato_info.get("email", "")
            firstname = contato_info.get("firstname", "")
            lastname = contato_info.get("lastname", "")
            contato_str = f"Nome: {firstname} {lastname}, Email: {email}"
        else:
            contato_str = str(contato_info)

        # Prompt estruturado para garantir resposta precisa
        prompt = (
            "Você é um assistente especialista em qualificação de leads e limpeza de CRM.\n"
            "Analise as seguintes informações do contato:\n"
            f"'{contato_str}'\n\n"
            "Regras de avaliação:\n"
            "1. Responda 'REMOVER' se o e-mail for claramente inválido, um e-mail temporário, "
            "um endereço de teste (ex: test@test.com, asdf@gmail.com), spam ou contiver palavrões/caracteres aleatórios.\n"
            "2. Responda 'MANTER' se parecer um contato real ou legítimo.\n\n"
            "Sua resposta DEVE começar OBRIGATORIAMENTE com a palavra 'REMOVER' ou 'MANTER', "
            "seguida de uma breve justificativa de uma frase."
        )

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            print(f"❌ Erro ao analisar contato com o Gemini: {e}")
            return "MANTER (Erro na análise)"