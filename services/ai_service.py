import os
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def enviar_alerta_discord(contact_id: str, email: str, properties: dict) -> bool:
    """
    Envia uma notificação formatada para o canal do Discord via Webhook.
    """
    if not DISCORD_WEBHOOK_URL:
        print("[ALERTA] DISCORD_WEBHOOK_URL não configurada no .env")
        return False

    nome = properties.get("firstname", "Não informado")
    telefone = properties.get("phone", "Não informado")

    payload = {
        "embeds": [
            {
                "title": "🚨 Lead com Dados Incompletos / Erro",
                "color": 15158332,
                "fields": [
                    {"name": "ID HubSpot", "value": str(contact_id), "inline": True},
                    {"name": "E-mail", "value": str(email), "inline": True},
                    {"name": "Nome", "value": str(nome), "inline": True},
                    {"name": "Telefone", "value": str(telefone), "inline": True}
                ],
                "footer": {"text": "HubCleaner AI • Sistema de Higienização"}
            }
        ]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        return response.status_code == 204
    except Exception as e:
        print(f"[ERRO] Falha ao enviar Webhook do Discord: {e}")
        return False