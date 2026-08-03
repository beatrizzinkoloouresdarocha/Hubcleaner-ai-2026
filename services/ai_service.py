import os
from hubspot import HubSpot

class HubSpotService:
    def __init__(self):
        token = os.getenv("HUBSPOT_ACCESS_TOKEN")
        if not token:
            print("⚠️ ATENÇÃO: HUBSPOT_ACCESS_TOKEN não foi encontrado no .env!")
        self.client = HubSpot(access_token=token)

    def buscar_contatos(self):
        try:
            # Solicita os contatos trazendo as propriedades necessárias
            resposta = self.client.crm.contacts.get_all(
                properties=["email", "firstname", "lastname"]
            )
            
            contatos_limpos = []

            for contato in resposta:
                # Extrai o dicionário de propriedades do objeto SDK
                props = getattr(contato, 'properties', {}) or {}
                
                # Monta o dicionário nativo com ID e atributos
                contato_dict = {
                    'id': getattr(contato, 'id', None),
                    'email': props.get('email', 'sem-email'),
                    'firstname': props.get('firstname', ''),
                    'lastname': props.get('lastname', '')
                }
                
                contatos_limpos.append(contato_dict)

            return contatos_limpos

        except Exception as e:
            print(f"❌ Erro ao buscar contatos no HubSpot: {e}")
            return []

    def deletar_contato(self, contato_id):
        try:
            self.client.crm.contacts.basic_api.archive(contact_id=str(contato_id))
            print(f"✅ Contato ID {contato_id} removido com sucesso.")
            return True
        except Exception as e:
            print(f"❌ Erro ao deletar contato ID {contato_id}: {e}")
            return False