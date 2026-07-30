import os
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInputForCreate

class HubSpotService:
    def __init__(self):
        # Conecta na API usando o token salvo no arquivo .env
        self.access_token = os.getenv("HUBSPOT_ACCESS_TOKEN")
        self.client = HubSpot(access_token=self.access_token)

    def buscar_contatos(self, limit=50):
        """Busca os contatos mais recentes no HubSpot CRM."""
        try:
            response = self.client.crm.contacts.basic_api.get_page(
                limit=limit,
                properties=["firstname", "lastname", "email", "phone", "hs_object_id"]
            )
            return response.results
        except Exception as e:
            print(f"Erro ao buscar contatos no HubSpot: {e}")
            return []

    def deletar_contato(self, contact_id):
        """Deleta um contato pelo ID no HubSpot."""
        try:
            self.client.crm.contacts.basic_api.archive(contact_id=contact_id)
            print(f"Contato {contact_id} removido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao deletar contato {contact_id}: {e}")
            return False