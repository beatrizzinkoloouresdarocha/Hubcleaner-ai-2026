import os
from hubspot import HubSpot

class HubSpotService:
    def __init__(self):
        token = os.getenv("HUBSPOT_ACCESS_TOKEN")
        self.client = HubSpot(access_token=token)

    def buscar_contatos(self):
        try:
            # Solicita explicitamente os campos de e-mail e nome
            api_response = self.client.crm.contacts.get_all(
                properties=["email", "firstname", "lastname"]
            )
            
            contatos_formatados = []
            for contato in api_response:
                props = contato.properties or {}
                contatos_formatados.append({
                    "id": contato.id,
                    "email": props.get("email", ""),
                    "firstname": props.get("firstname", ""),
                    "lastname": props.get("lastname", "")
                })
            
            return contatos_formatados
        except Exception as e:
            print(f"Erro ao buscar contatos no HubSpot: {e}")
            return []