# Consulta Jurídica com Selenium

Projeto de estudos em Python para automatizar uma consulta jurídica simulada em páginas HTML locais.

A automação lê uma planilha com dados de processos, acessa uma página de pesquisa, seleciona o estado, preenche os campos do formulário e registra na planilha se o processo foi encontrado ou não.

## Objetivo de aprendizado

Este projeto foi criado para praticar:

- automação de navegador com Selenium;
- leitura e atualização de planilhas com Pandas;
- interação com páginas HTML locais;
- uso de alertas do navegador;
- organização básica de um projeto Python para GitHub.

## Tecnologias utilizadas

- Python
- Selenium
- WebDriver Manager
- Pandas
- OpenPyXL
- HTML, CSS e JavaScript

## Funcionalidades

- Abre uma página HTML local que simula um sistema de pesquisa jurídica.
- Seleciona o estado informado na planilha.
- Preenche os campos: nome da parte, advogado e número do processo.
- Clica no botão de pesquisa.
- Lê o alerta de retorno.
- Atualiza a coluna `Status` da planilha com:
  - `Encontrado`;
  - `Não encontrado`;
  - ou mensagem de erro, caso ocorra alguma falha.
- Salva uma nova planilha com o resultado da execução.

## Estrutura do projeto

```text
consulta-juridica-selenium/
├── data/
│   ├── input/
│   │   └── processos_exemplo.xlsx
│   └── output/
│       └── .gitkeep
├── site/
│   ├── index.html
│   └── pesquisa_estadual.html
├── src/
│   └── main.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Como executar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/consulta-juridica-selenium.git
cd consulta-juridica-selenium
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute o projeto:

```bash
python src/main.py
```

5. Após a execução, o arquivo de saída será criado em:

```text
data/processos_resultado.xlsx
```

## Formato esperado da planilha

A planilha de entrada deve conter as seguintes colunas:

| Nome | Advogado | Processo | Cidade | Status |
|---|---|---|---|---|

Exemplo:

| Nome | Advogado | Processo | Cidade | Status |
|---|---|---|---|---|
| Lira | Alon Lawyer | PC6592 | Distrito Federal | |
| João | Lawyer Alon | EB3792 | Rio de Janeiro | |

A coluna `Cidade` precisa ter o mesmo texto exibido no menu da página HTML, por exemplo:

- Distrito Federal
- Rio de Janeiro
- São Paulo

## Observações

Este projeto usa páginas HTML locais apenas para fins de estudo. Ele não consulta sistemas jurídicos reais.

O resultado da pesquisa é simulado pela página `pesquisa_estadual.html`, que retorna aleatoriamente se um processo foi encontrado ou não. Portanto, o foco do projeto é praticar a automação, não obter dados jurídicos reais.