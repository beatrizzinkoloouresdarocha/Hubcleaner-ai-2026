from dotenv import load_dotenv
from services.chat_service import ChatService

load_dotenv()

chat = ChatService()
print("🧪 Testando envio de notificação individual...")

# Teste com dados fictícios
try:
    chat.enviar_notificacao(
        total_analisados=5,
        total_removidos=2,
        contatos_removidos_lista=["teste1@exemplo.com", "teste2@exemplo.com"]
    )
    print("✅ Notificação de teste enviada com sucesso!")
except Exception as e:
    print(f"❌ Falha ao enviar notificação: {e}")