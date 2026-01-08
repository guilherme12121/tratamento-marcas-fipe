# 🚗 Atualizador de Marcas FIPE

Este projeto é uma ferramenta em Python desenvolvida para automatizar a atualização do cadastro de marcas de veículos.

### 📋 O que ele faz?

1. Lê o seu banco de dados atual (`veiculo_marca.csv`).
2. Lê o arquivo oficial mais recente da FIPE em formato SQL (`.sql`).
3. Compara as duas listas.
4. Gera um novo arquivo Excel/CSV apenas com as **marcas novas** que ainda não estão cadastradas.
5. O arquivo final já vem formatado com separador de ponto e vírgula (`;`) para abrir corretamente no Excel brasileiro.

---

### 🛠️ Pré-requisitos

Para rodar este projeto, você precisa ter instalado no seu computador:

* **Python** (versão 3 ou superior).
* **VS Code** (ou outro editor de código).
* **Biblioteca Pandas** (instruções abaixo).

---

### 📂 Organização da Pasta

Certifique-se de que a sua pasta (ex: `tratamento_marca`) contenha os seguintes arquivos juntos:

1. `atualizar_marcas.py` (O código Python).
2. `veiculo_marca.csv` (Seu arquivo antigo/atual).
3. `fipe-02122025-MSSQL.sql` (O arquivo novo baixado da FIPE).

---

### 🚀 Instalação (Primeira vez)

Se você nunca rodou o projeto antes, precisa instalar a biblioteca de análise de dados.

1. Abra a pasta do projeto no VS Code.
2. Abra o Terminal (**Terminal > New Terminal**).
3. Digite o comando abaixo e aperte Enter:

```bash
py -m pip install pandas

```

*(Se o comando acima der erro, tente apenas `pip install pandas`)*

---

### ▶️ Como Rodar

Sempre que chegar uma planilha nova da FIPE:

1. Coloque o arquivo novo na pasta.
2. Abra o arquivo `atualizar_marcas.py` no VS Code.
3. Vá até o final do código, na seção **CONFIGURAÇÃO**, e atualize o nome do arquivo se necessário:
```python
# Exemplo:
arquivo_novo_sql = 'nome_do_arquivo_novo.sql'

```


4. Rode o script clicando no botão **Play** (▷) ou digitando no terminal:
```bash
py atualizar_marcas.py

```



---

### 📤 Resultado

Após rodar, um novo arquivo será criado na mesma pasta:

* **Nome:** `novas_marcas_consolidado.csv`
* **Como abrir:** Dê dois cliques para abrir no Excel.
* **Conteúdo:** Contém apenas as marcas inéditas, com IDs sequenciais gerados automaticamente.

---

### 🆘 Solução de Problemas Comuns

* **Erro "File not found":** Verifique se o nome do arquivo no código está *exatamente* igual ao nome do arquivo na pasta (cuidado com `.sql`, `.csv` e `.txt` ocultos).
* **Erro de "pip não reconhecido":** Certifique-se de usar `py -m pip ...` ou reinstale o Python marcando a opção "Add to PATH".
* **Acentos estranhos no Excel:** O script salva em `utf-8-sig`. Se ainda assim der erro, tente abrir o Excel em branco, ir em "Dados > Obter Dados de Texto/CSV" e selecionar o arquivo.