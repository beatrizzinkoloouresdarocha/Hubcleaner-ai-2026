import os
import requests


def enviar_alerta_discord(contato_id: str, email: str, alteracoes: dict) -> bool:
    """Envia uma notificação formatada para o canal do Discord através de um Webhook."""
    url_webhook = os.getenv("DISCORD_WEBHOOK_URL")

    if not url_webhook:
        print("⚠️ Variável 'DISCORD_WEBHOOK_URL' não configurada.")
        return False

    campos_formatados = "\n".join(
        [f"• **{chave}**: `{valor}`" for chave, valor in alteracoes.items()]
    )

    payload = {
        "embeds": [
            {
                "title": "🧹 HubCleaner AI - Contato Atualizado",
                "color": 3066993,
                "fields": [
                    {
                        "name": "👤 Contato",
                        "value": f"**Email:** {email}\n**ID HubSpot:** `{contato_id}`",
                        "inline": False,
                    },
                    {
                        "name": "📝 Campos Normalizados",
                        "value": campos_formatados if campos_formatados else "Nenhuma alteração registrada.",
                        "inline": False,
                    },
                ],
                "footer": {"text": "HubCleaner AI Automation"},
            }
        ]
    }

    try:
        response = requests.post(url_webhook, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar notificação para o Discord: {e}")
        return False