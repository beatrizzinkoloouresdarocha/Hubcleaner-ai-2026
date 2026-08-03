import os
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class ResultadoAnaliseContato(BaseModel):
    valido: bool = Field(description="Indica se o contato é um lead válido (True) ou inválido/spam/teste (False)")
    motivo: str = Field(description="Explicação sucinta sobre o motivo da classificação")
    categoria: str = Field(description="Categoria do contato: Ex: Lead Real, Spam, E-mail Temporário, Teste, Nome Fictício")

class AIService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ ATENÇÃO: GEMINI_API_KEY não foi encontrada no .env!")
        self.client = genai.Client(api_key=api_key)

    def _extrair_propriedade(self, props, chave: str, default: str = "") -> str:
        """Auxiliar para extrair valores de dicionários ou objetos com segurança."""
        if isinstance(props, dict):
            valor = props.get(chave, default)
        else:
            valor = getattr(props, chave, default)
        return valor if valor is not None else default

    def analisar_contato(self, contato) -> ResultadoAnaliseContato:
        # Extração segura de propriedades do objeto ou dicionário do HubSpot
        if isinstance(contato, dict):
            props = contato.get('properties', contato)
        else:
            props = getattr(contato, 'properties', contato) or {}

        email = self._extrair_propriedade(props, 'email', '')
        firstname = self._extrair_propriedade(props, 'firstname', '')
        lastname = self._extrair_propriedade(props, 'lastname', '')

        nome = f"{firstname} {lastname}".strip() or "Não informado"

        # Prompt otimizado para classificação mais precisa
        prompt = f"""
        Você é um auditor de qualidade de leads de CRM.
        Analise os dados abaixo e classifique o contato:

        - Nome completo: {nome}
        - E-mail: {email}

        Critérios de avaliação:
        1. Marque como INVÁLIDO (`valido = False`) se:
           - O nome ou e-mail contiver sequências aleatórias ou testes (ex: "asdf", "teste", "123").
           - O domínio for descartável ou temporário (ex: mailinator, tempmail, guerrilla).
           - O e-mail for obviamente fictício ou malformado.
        2. Marque como VÁLIDO (`valido = True`) se parecer um contato humano legítimo.
        """

        # Chamada ao modelo oficial Gemini 1.5 Flash
        resposta = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ResultadoAnaliseContato,
                temperature=0.1,  # Baixa temperatura para respostas mais consistentes e determinísticas
            )
        )

        return ResultadoAnaliseContato.model_validate_json(resposta.text)