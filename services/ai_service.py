import requests
import os

class ChatService:
    def __init__(self):
        # Defina DISCORD_WEBHOOK_URL no seu arquivo .env
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def enviar_resumo(self, total_analisados, total_remover):
        if not self.webhook_url or not self.webhook_url.startswith("http"):
            print("Erro: URL do Webhook do Discord não está configurada corretamente no .env")
            return

        mensagem = {
            "content": f"🚨 **HubCleaner AI - Relatório de Varredura** 🚨\n\n"
                       f"📊 **Total de contatos analisados:** {total_analisados}\n"
                       f"🗑️ **Contatos recomendados para remoção:** {total_remover}"
        }

        try:
            response = requests.post(self.webhook_url, json=mensagem)
            if response.status_code == 204:
                print("✅ Alerta enviado com sucesso para o Discord!")
            else:
                print(f"Erro ao enviar para o Discord: Status {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Erro ao conectar com o Discord: {e}")