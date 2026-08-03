import os
import requests

class ChatService:
    def __init__(self):
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def enviar_notificacao(self, mensagem_ou_total, total_remover=None):
        if not self.webhook_url or not self.webhook_url.startswith("http"):
            print("⚠️ URL do Webhook do Discord não configurada ou inválida no .env")
            return

        # Se for passado o número total e o número para remover
        if isinstance(mensagem_ou_total, int) and total_remover is not None:
            texto = (
                f"🚨 **HubCleaner AI - Relatório de Varredura** 🚨\n\n"
                f"📊 **Total de contatos analisados:** {mensagem_ou_total}\n"
                f"🗑️ **Contatos para remoção/spam:** {total_remover}"
            )
        else:
            # Se for passada uma string direta
            texto = str(mensagem_ou_total)

        payload = {"content": texto}

        try:
            response = requests.post(self.webhook_url, json=payload)
            if response.status_code in [200, 204]:
                print("✅ Alerta enviado com sucesso para o Discord!")
            else:
                print(f"Erro ao enviar para o Discord: Status {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Erro na conexão com o Discord: {e}")