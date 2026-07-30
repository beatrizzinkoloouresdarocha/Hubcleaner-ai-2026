import os
from dotenv import load_dotenv
from services.hubspot_service import HubSpotService
from services.ai_service import AIService
from services.chat_service import ChatService

load_dotenv()

def executar_limpeza():
    print("🚀 Iniciando varredura no HubCleaner AI...")

    hubspot = HubSpotService()
    ai = AIService()
    chat = ChatService()

    contatos = hubspot.buscar_contatos()
    print(f"Encontrados {len(contatos)} contatos para análise.")

    contatos_para_remover = []

    for idx, contato in enumerate(contatos, start=1):
        print(f"Analisando contato {idx}/{len(contatos)}: {contato.get('email')}")
        resultado = ai.analisar_contato(contato)
        
        if "REMOVER" in resultado.upper():
            contatos_para_remover.append(contato)

    print("\n📤 Enviando resumo para o Discord...")
    chat.enviar_resumo(
        total_analisados=len(contatos),
        total_remover=len(contatos_para_remover)
    )

if __name__ == "__main__":
    executar_limpeza()