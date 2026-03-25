"""
BrasilAPI integration service for CNPJ queries.
"""

import requests
from typing import Optional, Dict, Any


# --- CONFIGURATION AREA ---
# If API changes version or URL, we only modify here
BASE_URL = "https://brasilapi.com.br/api/cnpj/v1"


def consultar_cnpj(cnpj_alvo: str) -> Optional[Dict[str, Any]]:
    """
    Query company data from BrasilAPI using CNPJ.

    Args:
        cnpj_alvo: CNPJ number (with or without formatting)

    Returns:
        Dictionary with company data or None if not found
    """
    # --- DATA CLEANING ---
    # Ensures only numbers, even if main.py sends with dots
    cnpj_limpo = cnpj_alvo.replace(".", "").replace("/", "").replace("-", "")

    # URL assembly using constant
    url = f"{BASE_URL}/{cnpj_limpo}"

    # Discrete print to not pollute terminal
    print(f"Consultando: {cnpj_limpo}...", end=" ")

    try:
        # --- SECURITY (TIMEOUT) ---
        # If API takes more than 10s, robot gives up to not hang the PC
        resposta = requests.get(url, timeout=10)

        # --- SUCCESS (200) ---
        if resposta.status_code == 200:
            dados = resposta.json()

            # STANDARDIZATION: Creates a clean dictionary for Excel
            empresa_formatada = {
                "cnpj": dados.get("cnpj", cnpj_limpo),
                "razao_social": dados.get("razao_social", "N/A"),
                "nome_fantasia": dados.get("nome_fantasia", ""),
                "uf": dados.get("uf", ""),
                "municipio": dados.get("municipio", ""),
                "logradouro": dados.get("logradouro", ""),
                "bairro": dados.get("bairro", ""),
                "cep": dados.get("cep", ""),
                "situacao": dados.get("descricao_situacao_cadastral", "N/A"),
                "data_abertura": dados.get("data_inicio_atividade", ""),
            }

            print("✅ Encontrada!")
            return empresa_formatada

        # --- ERROR TRANSLATION (Humanized) ---

        elif resposta.status_code == 429:
            print(
                "\n   ⏳ CALMA: O servidor pediu um tempo (Muitas consultas seguidas)."
            )
            print("      -> O robô vai pular este e tentar o próximo.")
            return None

        elif resposta.status_code == 404:
            print("\n   🔍 NÃO ENCONTRADO: Esse CNPJ não existe na Receita Federal.")
            return None

        elif resposta.status_code == 400:
            print("\n   ⚠️ CNPJ INVÁLIDO: O número parece estar errado ou incompleto.")
            return None

        elif resposta.status_code >= 500:
            print(
                "\n   ☁️ ERRO NO SERVIDOR: A BrasilAPI está fora do ar momentaneamente."
            )
            return None

        else:
            print(f"\n   ❌ Erro desconhecido: {resposta.status_code}")
            return None

    except requests.exceptions.Timeout:
        print("\n   🐢 DEMOROU DEMAIS: A conexão caiu ou o site está lento.")
        return None

    except Exception as e:
        print(f"\n   ❌ ERRO TÉCNICO: {e}")
        return None


if __name__ == "__main__":
    # Quick test with valid CNPJ
    print(consultar_cnpj("00000000000191"))  # Banco do Brasil
