import os
import time
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

    # Usando o nome correto do método: buscar_contatos()
    contatos = hubspot.buscar_contatos()
    print(f"Encontrados {len(contatos)} contatos para análise.")

    spams_detectados = []

    for contato in contatos:
        props = getattr(contato, "properties", {}) or {}
        email = props.get("email", "")
        firstname = props.get("firstname", "")
        lastname = props.get("lastname", "")
        nome_completo = f"{firstname} {lastname}".strip()

        if email:
            # Chama o método de análise
            is_spam = ai.analisar_contato_spam(email, nome_completo)
            
            if is_spam:
                spams_detectados.append(f"⚠️ {nome_completo} ({email})")
        
        # Pausa de 4 segundos para respeitar os limites do Gemini Free
        time.sleep(4)

    if spams_detectados:
        mensagem = "🚨 **Relatório de Leads Spam Encontrados:**\n" + "\n".join(spams_detectados)
        chat.enviar_notificacao(mensagem)
    else:
        chat.enviar_notificacao("✅ Varredura concluída! Nenhum contato suspeito foi identificado.")

if __name__ == "__main__":
    executar_limpeza()