from main import enviar_alerta_discord

print("🧪 Enviando mensagem de teste para o Discord...")

# Simulando uma alteração efetuada
contato_id_teste = "12345"
email_teste = "teste@exemplo.com"
alteracoes_teste = {
    "firstname": "Maria",
    "email": "maria@exemplo.com",
    "phone": "+5541999998888"
}

enviar_alerta_discord(contato_id_teste, email_teste, alteracoes_teste)