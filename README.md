# 📊 Business Intelligence Classes 📈

> 🇬🇧 **English** below · 🇧🇷 **Português** [mais abaixo](#-aulas-de-business-intelligence-pt-br-)

## 📈 What is Business Intelligence?

Business Intelligence is the practice of turning raw, messy data into decisions. It covers the whole path: collecting data from the wild (APIs, web scraping, public spreadsheets), cleaning and modeling it, storing it in a way that answers questions fast, and finally presenting it so a human can act on it.

**`If you cannot measure it, you cannot improve it. BI is the toolset that makes measuring possible.`**

## Why does this repository exist?

This is a public repository for my **Business Intelligence classes** at **SENAI**, so you can see every piece of code I write in class, and learn from it as well.

`Every class folder has its own README.md explaining what it does and how to run it.`

## 🗂️ Classes board

| Class | Description | Status |
|---|---|---|
| [Aula 02](aulas/aula02) | 🐼 Exploratory data analysis with Pandas over Brazilian parliamentary amendments. | ✅ Done |
| [Aula 04](aulas/aula04) | 🕷️ Web scraping with Scrapy: bus timetables from a sitemap, plus a heuristic to pick the best line. | ✅ Done |
| [Aula 05](aulas/aula05) | 🛒 Full ETL pipeline: scraper + BCB API + SQLite/SQLAlchemy + inflation report. | ✅ Done |
| [Aula 07](aulas/aula07) | 🧮 Feature Engineering and PCA from scratch over the World Bank WDI dataset. | ✅ Done |

## 🛠️ Tech stack

* **Language:** Python
* **Web Scraping:** Scrapy, Playwright, w3lib
* **Data:** Pandas, NumPy, Matplotlib, Seaborn
* **Database:** SQLite, SQLAlchemy
* **Version control:** Git and GitHub

## Suit yourself and clone the repository

```bash
git clone "https://github.com/gilas-byte/aulas-b.i."
```

and if the repository gets an update:

```bash
git pull
```

> ⚠️ **Heads up:** the heavy datasets (`EmendasParlamentares.csv`, the WDI files) are **not** versioned here — they are hundreds of megabytes. Each class README tells you where to download them.

**Thanks for visiting, happy studying!**

---

# 📊 Aulas de Business Intelligence (PT-BR) 📈

## 📈 O que é Business Intelligence?

Business Intelligence é a prática de transformar dados brutos e bagunçados em decisões. Cobre o caminho inteiro: coletar dados de onde eles estiverem (APIs, web scraping, planilhas públicas), limpar e modelar, guardar de um jeito que responda perguntas rápido, e por fim apresentar de forma que um humano consiga agir.

**`Se você não consegue medir, você não consegue melhorar. BI é o conjunto de ferramentas que torna a medição possível.`**

## Por que este repositório existe?

Este é um repositório público das minhas **aulas de Business Intelligence** no **SENAI**, para que você possa ver todos os códigos que faço em aula, e aprender com eles também.

`Toda pasta de aula tem o seu próprio README.md explicando o que faz e como rodar.`

## 🗂️ Quadro de aulas

| Aula | Descrição | Status |
|---|---|---|
| [Aula 02](aulas/aula02) | 🐼 Análise exploratória com Pandas sobre as Emendas Parlamentares. | ✅ Concluído |
| [Aula 04](aulas/aula04) | 🕷️ Web scraping com Scrapy: horários de ônibus a partir do sitemap, mais uma heurística para escolher a melhor linha. | ✅ Concluído |
| [Aula 05](aulas/aula05) | 🛒 Pipeline de ETL completo: scraper + API do BCB + SQLite/SQLAlchemy + relatório de inflação. | ✅ Concluído |
| [Aula 07](aulas/aula07) | 🧮 Feature Engineering e PCA na unha sobre o dataset WDI do Banco Mundial. | ✅ Concluído |

## 🛠️ Tecnologias e ferramentas

* **Linguagem:** Python
* **Web Scraping:** Scrapy, Playwright, w3lib
* **Dados:** Pandas, NumPy, Matplotlib, Seaborn
* **Banco de dados:** SQLite, SQLAlchemy
* **Controle de versão:** Git e GitHub

## 🚀 Como rodar qualquer aula

Cada aula é um projeto independente. O caminho é sempre o mesmo:

```bash
cd aulas/aulaXX

python -m venv .venv
source .venv/bin/activate      # Linux / macOS
# .venv\Scripts\activate       # Windows

```

Depois é só seguir o README daquela aula: ele traz o `pip install` exato e a ordem de execução dos scripts. A Aula 05 tem um `requirements.txt` com as versões travadas; as demais listam as dependências direto no README.

## Sinta-se à vontade para clonar o repositório

```bash
git clone "https://github.com/gilas-byte/aulas-b.i."
```

e se o repositório tiver alguma atualização:

```bash
git pull
```

> ⚠️ **Atenção:** os datasets pesados (`EmendasParlamentares.csv`, os arquivos do WDI) **não** estão versionados aqui — são centenas de megabytes. O README de cada aula diz onde baixar.

**Obrigado pela visita, bons estudos!**
