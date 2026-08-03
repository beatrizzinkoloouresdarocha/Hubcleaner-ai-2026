import json
import os
from pathlib import Path
import sys
import time
from typing import Optional

# 1. Ajuste no sys.path para evitar ModuleNotFoundError ao executar o script diretamente
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from google import genai
from google.genai import types
from google.genai.errors import ClientError
from pydantic import BaseModel, Field

# Módulos do projeto
from discord_service import enviar_alerta_discord
from hubspot_service import atualizar_contato_hubspot, buscar_contatos_hubspot

client = genai.Client()

MODELO = "gemini-2.0-flash"


class PropriedadesHubSpotOpcionais(BaseModel):
    firstname: Optional[str] = Field(
        default=None, description="Primeiro nome capitalizado."
    )
    lastname: Optional[str] = Field(
        default=None, description="Sobrenome capitalizado."
    )
    email: Optional[str] = Field(
        default=None, description="E-mail formatado em minúsculas."
    )
    phone: Optional[str] = Field(
        default=None, description="Telefone no formato E.164."
    )


def limpar_valores_nulos(dicionario: dict) -> dict:
    return {
        chave: valor for chave, valor in dicionario.items() if valor is not None
    }


def analisar_contato_opcional(dados_contato: dict) -> tuple[dict, bool]:
    """Analisa o contato no Gemini.

    Retorna uma tupla: (payload_hubspot, stop_execution)
    """
    prompt = f"""
    Análise os dados abaixo e retorne APENAS os campos que precisam de correção/padronização.
    Para campos corretos, retorne null.
    Dados: {dados_contato}
    """

    max_tentativas = 3
    for tentativa in range(max_tentativas):
        try:
            response = client.models.generate_content(
                model=MODELO,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=PropriedadesHubSpotOpcionais,
                    temperature=0.1,
                ),
            )
            dados_brutos = json.loads(response.text)
            return limpar_valores_nulos(dados_brutos), False

        except ClientError as e:
            if e.code == 429:
                print(
                    f"⚠️ Cota do Gemini excedida (429). Tentativa {tentativa + 1}/{max_tentativas}."
                )

                if "QuotaExceeded" in str(e) or "FreeTier" in str(e):
                    print(
                        "⛔ Cota diária/projeto do Free Tier atingida. Interrompendo execução."
                    )
                    return {}, True

                print("⏳ Aguardando 15s para estabilizar o limite de RPM...")
                time.sleep(15)
            else:
                print(f"❌ Erro na API do Gemini: {e}")
                break
        except Exception as e:
            print(f"❌ Erro inesperado no Gemini: {e}")
            break

    return {}, False


def executar_limpeza_contatos(limite_testes: Optional[int] = None):
    print("🚀 Iniciando varredura no HubCleaner AI...")

    # Tratamento isolado para a busca inicial de contatos
    try:
        contatos = buscar_contatos_hubspot()
    except Exception as e:
        print(f"❌ Erro fatal ao buscar contatos do HubSpot: {e}")
        return

    if limite_testes and limite_testes > 0:
        contatos = contatos[:limite_testes]
        print(f"🧪 Modo de teste ativado: limitando a {len(contatos)} contatos.")
    else:
        print(f"Encontrados {len(contatos)} contatos para análise.\n")

    for contato in contatos:
        contato_id = str(contato.get("id"))
        props = contato.get("properties", {})
        email = props.get("email") or contato.get("email", "Sem Email")

        print(f"\n🔍 Analisando contato: {email} (ID: {contato_id})...")
        payload_hubspot, cota_esgotada = analisar_contato_opcional(contato)

        if cota_esgotada:
            print("🛑 Processamento pausado devido ao limite de cota da API Gemini.")
            break

        if payload_hubspot:
            print(f"📝 Atualizações identificadas: {payload_hubspot}")

            # Tratamento isolado para atualização no HubSpot
            try:
                atualizar_contato_hubspot(contato_id, payload_hubspot)
                print(f"✅ Contato {contato_id} atualizado no HubSpot com sucesso.")
            except Exception as e:
                print(f"⚠️ Falha ao atualizar o contato {contato_id} no HubSpot: {e}")

            # Tratamento isolado para notificação no Discord
            try:
                enviar_alerta_discord(contato_id, email, payload_hubspot)
                print(f"📢 Alerta do contato {contato_id} enviado ao Discord.")
            except Exception as e:
                print(f"⚠️ Falha ao enviar alerta para o Discord ({email}): {e}")

        else:
            print("✨ Nenhum ajuste necessário para este contato.")

        # Pausa preventiva entre requisições
        time.sleep(5)


if __name__ == "__main__":
    executar_limpeza_contatos(limite_testes=2)