"""
Web scraping service using Selenium.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from typing import Optional


def capturar_texto_da_web(url_alvo: str) -> Optional[str]:
    """
    Capture text content from a web page using Selenium.

    Args:
        url_alvo: Target URL to scrape

    Returns:
        Text content from page body or empty string if error occurred
    """
    print(f" Iniciando navegador para acessar: {url_alvo} ")

    navegador = webdriver.Chrome()

    try:
        navegador.get(url_alvo)

        # Wait for page to load
        time.sleep(5)

        # Extract text from body element
        elemento_corpo = navegador.find_element(By.TAG_NAME, "body")
        texto_completo = elemento_corpo.text

        print(
            f" Texto capturado com sucesso! Tamanho: {len(texto_completo)} caracteres. "
        )
        return texto_completo

    except Exception as e:
        print(f" Erro ao acessar a página: {e} ")
        return ""

    finally:
        navegador.quit()


if __name__ == "__main__":
    url_teste = "https://www.gov.br/pt-br"
    print(capturar_texto_da_web(url_teste))
