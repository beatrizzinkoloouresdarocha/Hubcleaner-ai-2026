import os
import requests

class ChatService:
    def __init__(self):
        self.webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")

    def enviar_alerta_varredura(self, total_duplicados, emails_removidos):
        """Envia uma mensagem formatada para a sala do Google Chat."""
        if not self.webhook_url:
            print("Webhook do Google Chat não configurado no arquivo .env!")
            return False

        # Formatação do texto com Markdown suportado pelo Google Chat
        lista_emails = "\n".join([f"• `{email}`" for email in emails_removidos]) if emails_removidos else "Nenhum e-mail inválido detectado."
        
        mensagem = {
            "text": (
                "🚨 *HubCleaner AI - Relatório de Higienização de Dados*\n\n"
                f"📊 *Contatos duplicados mesclados/removidos:* `{total_duplicados}`\n"
                f"🗑️ *Contatos removidos (Spam/Inválido):*\n{lista_emails}\n\n"
                "✅ Varredura concluída com sucesso."
            )
        }

        try:
            response = requests.post(self.webhook_url, json=mensagem)
            if response.status_code == 200:
                print("Notificação enviada ao Google Chat com sucesso!")
                return True
            else:
                print(f"Erro ao enviar notificação: STATUS {response.status_code}")
                return False
        except Exception as e:
            print(f"Erro ao conectar com o Google Chat: {e}")
            return False
            return False