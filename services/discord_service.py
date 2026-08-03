import os
import requests

class DiscordService:
    def __init__(self):
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def enviar_alerta_remocao(self, email: str, motivo: str, origem: str):
        """Envia um embed formatado para o Discord ao remover um contato."""
        if not self.webhook_url:
            print("⚠️ URL do Discord Webhook não configurada no .env")
            return

        payload = {
            "embeds": [
                {
                    "title": "🧹 Contato Removido do CRM",
                    "color": 15158332,  # Cor vermelha/alerta em decimal
                    "fields": [
                        {"name": "E-mail", "value": email, "inline": True},
                        {"name": "Detectado por", "value": origem, "inline": True},
                        {"name": "Motivo", "value": motivo, "inline": False}
                    ],
                    "footer": {"text": "HubCleaner AI • Sistema de Limpeza de CRM"}
                }
            ]
        }

        try:
            requests.post(self.webhook_url, json=payload, timeout=5)
        except Exception as e:
            print(f"❌ Falha ao enviar notificação no Discord: {e}")