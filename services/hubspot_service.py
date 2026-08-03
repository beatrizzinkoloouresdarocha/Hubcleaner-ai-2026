import os
import requests
from dotenv import load_dotenv

load_dotenv()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_ACCESS_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_API_KEY}",
    "Content-Type": "application/json"
}

def buscar_contatos_hubspot():
    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    params = {"limit": 10, "properties": "firstname,lastname,email,phone"}
    try:
        res = requests.get(url, headers=HEADERS, params=params)
        if res.status_code == 200:
            return res.json().get("results", [])
        print(f"❌ Erro HubSpot ao buscar contatos: {res.status_code} - {res.text}")
        return []
    except Exception as e:
        print(f"❌ Exceção ao conectar no HubSpot: {e}")
        return []

def atualizar_contato_hubspot(contato_id: str, propriedades: dict):
    url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contato_id}"
    payload = {"properties": propriedades}
    try:
        res = requests.patch(url, headers=HEADERS, json=payload)
        return res.status_code in [200, 204]
    except Exception as e:
        print(f"❌ Erro ao atualizar contato {contato_id}: {e}")
        return False