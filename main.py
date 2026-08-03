import os
from dotenv import load_dotenv
from services.hubspot_service import HubSpotService
from services.ai_service import AIService

load_dotenv()

def executar_limpeza():
    print("🚀 Iniciando varredura no HubCleaner AI...")
    
    hubspot = HubSpotService()
    ai = AIService()

    contatos = hubspot.buscar_contatos()
    print(f"Encontrados {len(contatos)} contatos para análise.")

    for contato in contatos:
        # Garante a leitura do e-mail seja 'contato' um dict ou um objeto do SDK
        if isinstance(contato, dict):
            email = contato.get('email', 'sem-email')
            contato_id = contato.get('id')
        else:
            props = getattr(contato, 'properties', {}) or {}
            email = props.get('email', 'sem-email')
            contato_id = getattr(contato, 'id', None)

        print(f"Analisando contato: {email} (ID: {contato_id})")
        
        # Análise de IA
        resultado = ai.analisar_contato(contato)
        print(f"Resultado IA: {resultado}")

if __name__ == "__main__":
    executar_limpeza()