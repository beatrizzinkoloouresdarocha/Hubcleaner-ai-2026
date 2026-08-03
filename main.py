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

    contatos_removidos_lista = []

    for idx, contato in enumerate(contatos, start=1):
        email = contato.get('email', 'sem-email')
        print(f"Analisando contato {idx}/{len(contatos)}: {email}")
        
        resultado = ai.analisar_contato(contato)
        
        if "REMOVER" in resultado.upper():
            print(f"⚠️ Identificado para remoção: {email}")
            
            # Deleta no HubSpot
            sucesso = hubspot.deletar_contato(contato.get('id'))
            if sucesso:
                contatos_removidos_lista.append(email)

    print("\n📤 Enviando resumo para o Discord...")
    # Chama o método correto com a lista de e-mails removidos
    chat.enviar_notificacao(
        mensagem_ou_total=len(contatos),
        total_remover=len(contatos_removidos_lista),
        contatos_removidos_lista=contatos_removidos_lista
    )

if __name__ == "__main__":
    executar_limpeza()