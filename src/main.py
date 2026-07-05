from pathlib import Path
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


BASE_DIR = Path(__file__).resolve().parents[1]

ARQUIVO_SITE = BASE_DIR / "site" / "index.html"
ARQUIVO_ENTRADA = BASE_DIR / "data" / "input" / "processos_exemplo.xlsx"
ARQUIVO_SAIDA = BASE_DIR / "data" / "output" / "processos_resultado.xlsx"

TEMPO_MAXIMO_ALERTA = 15

COLUNAS_OBRIGATORIAS = ["Nome", "Advogado", "Processo", "Cidade"]

ESTADOS = {
    "DF": "Distrito Federal",
    "RJ": "Rio de Janeiro",
    "SP": "São Paulo",
    "Distrito Federal": "Distrito Federal",
    "Rio de Janeiro": "Rio de Janeiro",
    "São Paulo": "São Paulo",
}


def iniciar_navegador():
    """Inicia o navegador Chrome usando o WebDriver Manager."""
    servico = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=servico)


def esperar_alerta(driver, tempo_maximo=TEMPO_MAXIMO_ALERTA):
    """Aguarda até que um alerta apareça na tela."""
    inicio = time.time()

    while time.time() - inicio < tempo_maximo:
        try:
            return driver.switch_to.alert
        except NoAlertPresentException:
            time.sleep(1)

    raise TimeoutError("O alerta não apareceu dentro do tempo esperado.")


def tratar_valor(valor):
    """Evita preencher campos com valores nulos da planilha."""
    if pd.isna(valor):
        return ""
    return str(valor)


def obter_nome_estado(cidade):
    """Converte a sigla ou o nome do estado para o texto usado no site."""
    cidade = tratar_valor(cidade).strip()

    if cidade not in ESTADOS:
        raise ValueError(f"Estado não reconhecido na planilha: {cidade}")

    return ESTADOS[cidade]


def validar_planilha(tabela):
    """Confere se a planilha possui as colunas necessárias."""
    colunas_faltando = []

    for coluna in COLUNAS_OBRIGATORIAS:
        if coluna not in tabela.columns:
            colunas_faltando.append(coluna)

    if colunas_faltando:
        raise ValueError(f"Colunas ausentes na planilha: {colunas_faltando}")


def consultar_processo(driver, linha):
    """Consulta um processo no site local e retorna o status encontrado."""
    driver.get(ARQUIVO_SITE.as_uri())

    aba_inicial = driver.current_window_handle
    abas_antes = set(driver.window_handles)
    nova_aba = None

    try:
        menu = driver.find_element(By.CLASS_NAME, "dropdown-menu")
        ActionChains(driver).move_to_element(menu).perform()

        cidade = obter_nome_estado(linha["Cidade"])
        driver.find_element(By.PARTIAL_LINK_TEXT, cidade).click()

        while len(driver.window_handles) == len(abas_antes):
            time.sleep(0.5)

        nova_aba = [aba for aba in driver.window_handles if aba not in abas_antes][0]
        driver.switch_to.window(nova_aba)

        driver.find_element(By.ID, "nome").send_keys(tratar_valor(linha["Nome"]))
        driver.find_element(By.ID, "advogado").send_keys(tratar_valor(linha["Advogado"]))
        driver.find_element(By.ID, "numero").send_keys(tratar_valor(linha["Processo"]))
        driver.find_element(By.CLASS_NAME, "registerbtn").click()

        primeiro_alerta = esperar_alerta(driver)
        primeiro_alerta.accept()

        segundo_alerta = esperar_alerta(driver)
        texto_alerta = segundo_alerta.text

        if "Processo encontrado com sucesso" in texto_alerta:
            status = "Encontrado"
        else:
            status = "Não encontrado"

        segundo_alerta.accept()

        return status

    finally:
        if nova_aba and nova_aba in driver.window_handles:
            driver.close()

        if aba_inicial in driver.window_handles:
            driver.switch_to.window(aba_inicial)


def main():
    """Executa a automação para todos os processos da planilha."""
    print("Automação iniciada...")

    if not ARQUIVO_ENTRADA.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {ARQUIVO_ENTRADA}")

    ARQUIVO_SAIDA.parent.mkdir(parents=True, exist_ok=True)

    tabela = pd.read_excel(ARQUIVO_ENTRADA, dtype=str)

    validar_planilha(tabela)

    if "Status" not in tabela.columns:
        tabela["Status"] = ""
    else:
        tabela["Status"] = tabela["Status"].astype("object")

    driver = iniciar_navegador()

    try:
        for indice, linha in tabela.iterrows():
            processo = tratar_valor(linha["Processo"])
            print(f"Consultando processo {indice + 1}: {processo}")

            try:
                tabela.loc[indice, "Status"] = consultar_processo(driver, linha)
            except Exception as erro:
                tabela.loc[indice, "Status"] = f"Erro: {erro}"

        tabela.to_excel(ARQUIVO_SAIDA, index=False)

        print("Automação finalizada.")
        print(f"Resultado salvo em: {ARQUIVO_SAIDA}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
