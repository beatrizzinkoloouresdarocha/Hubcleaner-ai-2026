import os
import time
from dotenv import load_dotenv
from services.hubspot_service import HubSpotService
from services.ai_service import AIService, ResultadoAnaliseContato

load_dotenv()

def executar_limpeza():
    print("🚀 Iniciando varredura no HubCleaner AI...")
    
    hubspot = HubSpotService()
    ai = AIService()

    contatos = hubspot.buscar_contatos()
    print(f"Encontrados {len(contatos)} contatos para análise.")

    for contato in contatos:
        if isinstance(contato, dict):
            props = contato.get('properties', contato)
            email = props.get('email', 'sem-email') if isinstance(props, dict) else 'sem-email'
            contato_id = contato.get('id')
        else:
            props = getattr(contato, 'properties', {}) or {}
            email = props.get('email', 'sem-email') if isinstance(props, dict) else getattr(props, 'email', 'sem-email')
            contato_id = getattr(contato, 'id', None)

        print(f"\nAnalisando contato: {email} (ID: {contato_id})")
        
        sucesso = False
        tentativas = 0
        max_tentativas = 3
        tempo_espera = 20  # Segundos de pausa inicial ao tomar erro 429

        resultado: ResultadoAnaliseContato = None

        while not sucesso and tentativas < max_tentativas:
            try:
                resultado = ai.analisar_contato(contato)
                sucesso = True
            except Exception as e:
                erro_msg = str(e)
                if "429" in erro_msg or "RESOURCE_EXHAUSTED" in erro_msg:
                    tentativas += 1
                    print(f"⚠️ Cota do Gemini atingida (429). Aguardando {tempo_espera}s para tentar novamente (Tentativa {tentativas}/{max_tentativas})...")
                    time.sleep(tempo_espera)
                    tempo_espera *= 2
                else:
                    print(f"❌ Erro ao analisar contato {email}: {e}")
                    break

        if resultado:
            print(f"📌 Classificação: {'VÁLIDO' if resultado.valido else 'INVÁLIDO'}")
            print(f"📌 Categoria: {resultado.categoria}")
            print(f"📌 Motivo: {resultado.motivo}")

            if not resultado.valido and contato_id:
                print(f"⚠️ Contato marcado como inválido. Removendo do HubSpot...")
                hubspot.deletar_contato(contato_id)

        # Delay de segurança de 4 segundos entre cada chamada (garante no máx 15 requisições/minuto)
        time.sleep(4)

if __name__ == "__main__":
    executar_limpeza()