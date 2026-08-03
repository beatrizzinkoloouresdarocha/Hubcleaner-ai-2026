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
    total_analisados = len(contatos)
    print(f"Encontrados {total_analisados} contatos para análise.")

    contatos_removidos_lista = []

    for idx, contato in enumerate(contatos, start=1):
        email = contato.get('email', 'sem-email')
        firstname = contato.get('firstname', '')
        lastname = contato.get('lastname', '')
        contato_id = contato.get('id')

        print(f"\nAnalisando contato {idx}/{total_analisados}: {email}")
        
        info_contato = f"ID: {contato_id}, Nome: {firstname} {lastname}, Email: {email}"
        
        resultado = ai.analisar_contato(info_contato)
        print(f"Resultado IA: {resultado}")
        
        if "REMOVER" in str(resultado).upper():
            print(f"⚠️ Identificado para remoção: {email}")
            
            if contato_id:
                sucesso = hubspot.deletar_contato(contato_id)
                if sucesso:
                    contatos_removidos_lista.append(email)
            else:
                print(f"❌ Não foi possível remover {email}: ID do contato ausente.")

    print("\n📤 Enviando resumo das ações...")
    
    try:
        chat.enviar_notificacao(
            total_analisados=total_analisados,
            total_removidos=len(contatos_removidos_lista),
            contatos_removidos_lista=contatos_removidos_lista
        )
    except TypeError:
        chat.enviar_notificacao(
            mensagem_ou_total=total_analisados,
            total_remover=len(contatos_removidos_lista),
            contatos_removidos_lista=contatos_removidos_lista
        )

if __name__ == "__main__":
    executar_limpeza()