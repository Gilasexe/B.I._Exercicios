# 🛒 Aula 05 — Pipeline de ETL: Cesta Básica e Inflação

> A aula mais completa do repositório. Sai de "não tenho dado nenhum" e chega em "tenho um relatório em Excel e um gráfico de inflação".

## 🎯 O que essa aula faz

Monta um pipeline de BI de ponta a ponta para responder: **quanto custa a cesta básica hoje, e quanto ela custava nos últimos anos?**

Duas fontes de dados completamente diferentes se encontram no mesmo banco:

* **Preços de hoje** → raspados do site do Giassi Supermercados.
* **Inflação histórica** → puxada da API do Banco Central (série 433, IPCA mensal).

Cruzando os dois, o relatório reconstrói o preço da cesta de 2020 até 2026 aplicando o IPCA de trás para frente.

## 🔗 A arquitetura

```
database_schema.py  ──▶  cria o schema (SQLAlchemy)
                              │
        ┌─────────────────────┴─────────────────────┐
        ▼                                           ▼
   api_ipca.py                              scraper_giassi.py
 (API do Banco Central)                     (scraping do Giassi)
        │                                           │
        └─────────────────▶ dados_cesta_basica.db ◀─┘
                                    │
                                    ▼
                            relatorio_cesta.py
                                    │
                        ┌───────────┴───────────┐
                        ▼                       ▼
                  .xlsx formatados        gráfico .png
```

Cada script faz uma coisa só e se comunica pelo banco. Isso significa que você pode rerodar a análise sem raspar o site de novo, ou atualizar o IPCA sem mexer nos preços.

## 🗃️ O modelo de dados

Três tabelas, definidas com SQLAlchemy ORM em `database_schema.py`:

| Tabela | Papel |
|---|---|
| `categorias` | Os itens da cesta (arroz, feijão, óleo, açúcar, café, macarrão, farinha, sal). |
| `produtos` | Cada produto raspado, com marca, preço, unidade e data de coleta. Aponta para uma categoria. |
| `ipca_historico` | Série mensal do IPCA vinda do Banco Central. |

A separação `categorias` ↔ `produtos` é o que permite a pergunta central do relatório: *dentro da categoria "arroz", qual é o mais barato e qual é o mais caro?*

## 🕷️ Scraping educado

O `scraper_giassi.py` roda com freio de mão puxado — de propósito:

```python
custom_settings = {
    'DOWNLOAD_DELAY': 2,
    'RANDOMIZE_DOWNLOAD_DELAY': True,
    'CONCURRENT_REQUESTS': 1,
    'HTTPCACHE_ENABLED': True,
    'HTTPCACHE_EXPIRATION_SECS': 86400,
}
```

* **Delay de 2s + aleatoriedade + 1 requisição por vez** — não derruba nem irrita o servidor do supermercado.
* **Cache HTTP de 24h** — a segunda execução no mesmo dia lê do disco em vez de bater no site. Isso salva muito tempo enquanto você ajusta os seletores.

> 📌 A pasta de cache (`.scrapy/`) e o log (`scrapy_output.log`) **não** são versionados. São arquivos temporários que se regeneram sozinhos.

## 🧹 A limpeza no SQL

O scraper pega mais coisa do que deveria — buscar por "sal" traz "Aji-Sal", buscar por "café" traz "Bebida Láctea sabor Café". A filtragem acontece na consulta, em `relatorio_cesta.py`:

```sql
WHERE p.nome_marca NOT LIKE '%Margarina%'
  AND p.nome_marca NOT LIKE '%Tempero%'
  AND p.nome_marca NOT LIKE '%Aji-Sal%'
  ...
```

É uma lista de exclusão construída na mão, olhando os falsos positivos que apareceram. Não é elegante, mas é honesto: quem lê o código vê exatamente o que foi descartado e por quê.

## 📊 A regressão pelo IPCA

Para estimar o preço da cesta em anos passados, o relatório **desconta** a inflação ano a ano:

```python
preco_ano_anterior = preco_atual / (1 + taxa_ipca)
```

Repetindo isso de 2026 para trás até 2020, monta a série histórica. É uma aproximação — assume que a cesta acompanhou o IPCA geral, e não o índice específico de alimentos — mas é o suficiente para enxergar a tendência no gráfico.

## 📁 Arquivos

| Arquivo | O que é |
|---|---|
| `database_schema.py` | Modelo ORM e criação do banco SQLite. |
| `api_ipca.py` | Consome a API do BCB e popula `ipca_historico`, sem duplicar registros. |
| `scraper_giassi.py` | Spider que preenche `categorias` e `produtos`. |
| `relatorio_cesta.py` | Consulta, monta as cestas, gera os `.xlsx` e o gráfico. |
| `zipar_entrega.py` | Empacota tudo num `.zip` para entregar ao professor. |
| `requirements.txt` | Dependências travadas por versão. |
| `instrucoes.txt` | Bilhete original de entrega (mantido por histórico). |
| `resultados/` | Saídas geradas: as duas planilhas e o gráfico de inflação. |

## ▶️ Como rodar

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

**A ordem importa** — cada script depende do estado deixado pelo anterior:

```bash
python database_schema.py    # 1. cria as tabelas
python api_ipca.py           # 2. carrega o IPCA
python scraper_giassi.py     # 3. raspa os preços (demora, tem delay proposital)
python relatorio_cesta.py    # 4. gera relatórios e gráfico
```

## 📈 Resultados

A pasta `resultados/` traz a saída de uma execução real:

* `relatorio_cesta_menor_valor.xlsx` — a cesta mais barata possível.
* `relatorio_cesta_maior_valor.xlsx` — a cesta mais cara possível.
* `grafico_inflacao_cestas.png` — as duas curvas de 2020 a 2026.

## 💡 O que eu aprendi aqui

* Um pipeline dividido em scripts pequenos, conversando por um banco, é infinitamente mais fácil de debugar que um script gigante.
* Cache HTTP no scraper não é otimização, é sanidade mental — você vai rodar o spider dezenas de vezes ajustando seletor.
* Cruzar duas fontes independentes (scraping + API pública) é o que transforma "uma lista de preços" em "uma análise".
* ORM (SQLAlchemy) faz valer a pena mesmo num projeto pequeno: o schema vira documentação executável.
