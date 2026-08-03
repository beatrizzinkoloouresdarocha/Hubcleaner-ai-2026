import os
from dotenv import load_dotenv
from services.ai_service import AIService

# Carrega as variáveis do .env
load_dotenv()

def rodar_teste():
    print("🧪 Testando AIService com o Gemini...\n")
    ai = AIService()

    # Lista de contatos fictícios para validar as regras
    contatos_teste = [
        {"firstname": "João", "lastname": "Silva", "email": "joao.silva@gmail.com"},
        {"firstname": "Test", "lastname": "User", "email": "asdfghjk@mailinator.com"},
        {"firstname": "Maria", "lastname": "Oliveira", "email": "maria.teste123@gmail.com"},
        {"firstname": "Fake", "lastname": "Bot", "email": "test@test.com"}
    ]

    for idx, contato in enumerate(contatos_teste, start=1):
        email = contato["email"]
        nome = f"{contato['firstname']} {contato['lastname']}"
        print(f"[{idx}] Analisando: {nome} ({email})")
        
        # Testa passando o dicionário direto
        resultado = ai.analisar_contato(contato)
        print(f"   🤖 Resposta do Gemini:\n   {resultado}\n")
        print("-" * 50)

if __name__ == "__main__":
    rodar_teste()