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
        # Acessa o dicionário de propriedades caso seja um objeto do SDK da HubSpot
        props = getattr(contato, 'properties', contato) if hasattr(contato, 'properties') else contato

        # O ID fica na raiz do objeto (contato.id) ou no dicionário (contato.get('id'))
        contato_id = getattr(contato, 'id', None) or (contato.get('id') if isinstance(contato, dict) else None)

        email = props.get('email', 'sem-email') if isinstance(props, dict) else 'sem-email'
        firstname = props.get('firstname', '') if isinstance(props, dict) else ''
        lastname = props.get('lastname', '') if isinstance(props, dict) else ''

        print(f"Analisando contato {idx}/{total_analisados}: {email}")
        
        # Monta um resumo textual legível para enviar à IA
        info_contato = f"ID: {contato_id}, Nome: {firstname} {lastname}, Email: {email}"
        
        # Solicita a análise da IA
        resultado = ai.analisar_contato(info_contato)
        
        # Verifica a decisão da IA
        if "REMOVER" in str(resultado).upper():
            print(f"⚠️ Identificado para remoção: {email}")
            
            if contato_id:
                # Executa a remoção no HubSpot
                sucesso = hubspot.deletar_contato(contato_id)
                if sucesso:
                    contatos_removidos_lista.append(email)
            else:
                print(f"❌ Não foi possível remover {email}: ID do contato ausente.")

    print("\n📤 Enviando resumo das ações...")
    
    # Notifica o canal do Discord / Chat com o relatório final
    try:
        chat.enviar_notificacao(
            total_analisados=total_analisados,
            total_removidos=len(contatos_removidos_lista),
            contatos_removidos_lista=contatos_removidos_lista
        )
    except TypeError:
        # Fallback caso seu ChatService utilize assinaturas diferentes de parâmetros
        chat.enviar_notificacao(
            mensagem_ou_total=total_analisados,
            total_remover=len(contatos_removidos_lista),
            contatos_removidos_lista=contatos_removidos_lista
        )

if __name__ == "__main__":
    executar_limpeza()