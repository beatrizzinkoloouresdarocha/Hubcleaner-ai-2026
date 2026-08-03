import unittest
from dotenv import load_dotenv
from services.ai_service import AIService

# Carrega as variáveis do .env (necessário para a GEMINI_API_KEY)
load_dotenv()

class TestAIService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Inicializa o serviço de IA uma única vez para a bateria de testes."""
        cls.ai_service = AIService()

    def test_lead_valido(self):
        """Testa se a IA reconhece um contato real com nome e e-mail legítimos."""
        contato_real = {
            "properties": {
                "firstname": "Beatriz",
                "lastname": "Rocha",
                "email": "beatriz.rocha@empresa.com.br"
            }
        }
        resultado = self.ai_service.analisar_contato(contato_real)
        
        print(f"\n[TESTE LEAD VÁLIDO] -> Valido: {resultado.valido} | Categoria: {resultado.categoria} | Motivo: {resultado.motivo}")
        self.assertTrue(resultado.valido, "O lead deveria ter sido marcado como válido.")

    def test_email_teste_ou_ficticio(self):
        """Testa se a IA identifica e-mails óbvios de teste ou spam."""
        contato_teste = {
            "properties": {
                "firstname": "Teste",
                "lastname": "da Silva",
                "email": "teste12345@mailinator.com"
            }
        }
        resultado = self.ai_service.analisar_contato(contato_teste)

        print(f"\n[TESTE E-MAIL DESKARTÁVEL/TESTE] -> Valido: {resultado.valido} | Categoria: {resultado.categoria} | Motivo: {resultado.motivo}")
        self.assertFalse(resultado.valido, "O lead deveria ter sido marcado como inválido.")

    def test_nome_com_caracteres_aleatorios(self):
        """Testa se a IA identifica nomes com caracteres de teclado (ex: asdfgh)."""
        contato_junk = {
            "properties": {
                "firstname": "Asdfgh",
                "lastname": "Qwerty",
                "email": "asdfgh.qwerty@gmail.com"
            }
        }
        resultado = self.ai_service.analisar_contato(contato_junk)

        print(f"\n[TESTE NOME FICTÍCIO] -> Valido: {resultado.valido} | Categoria: {resultado.categoria} | Motivo: {resultado.motivo}")
        self.assertFalse(resultado.valido, "O lead deveria ter sido marcado como inválido devido ao nome aleatório.")

if __name__ == "__main__":
    unittest.main()