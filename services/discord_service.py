import os
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def enviar_alerta_discord(contact_id: str, email: str, properties: dict) -> bool:
    if not DISCORD_WEBHOOK_URL:
        print("[ALERTA] DISCORD_WEBHOOK_URL nao configurada no .env")
        return False

    nome = properties.get("firstname", "Nao informado")
    telefone = properties.get("phone", "Nao informado")

    payload = {
        "embeds": [
            {
                "title": "Lead com Dados Incompletos / Erro",
                "color": 15158332,
                "fields": [
                    {"name": "ID HubSpot", "value": str(contact_id), "inline": True},
                    {"name": "E-mail", "value": str(email), "inline": True},
                    {"name": "Nome", "value": str(nome), "inline": True},
                    {"name": "Telefone", "value": str(telefone), "inline": True}
                ],
                "footer": {"text": "HubCleaner AI - Sistema de Higienizacao"}
            }
        ]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        return response.status_code in (200, 204)
    except Exception as e:
        print(f"[ERRO] Falha ao enviar Webhook do Discord: {e}")
        return False
