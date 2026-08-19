# 🐼 Aula 02 — Análise Exploratória com Pandas

> Primeira aula "de verdade" com dados: pegar uma planilha pública gigante, limpar o que veio torto e responder perguntas com ela.

## 🎯 O que essa aula faz

Trabalhamos com o dataset de **Emendas Parlamentares** do Portal da Transparência do Governo Federal. O arquivo vem sujo: valores monetários chegam como texto no padrão brasileiro (`1.234,56`), o que faz o Pandas ler tudo como `string` e impede qualquer cálculo.

A aula cobre o ciclo básico de BI:

1. **Ingestão** — ler um CSV com encoding e separador não-padrão.
2. **Limpeza** — converter valores brasileiros em números de verdade.
3. **Análise** — agrupar, agregar e responder perguntas de negócio.
4. **Visualização** — gerar gráficos com Matplotlib.

## 📁 Arquivos

| Arquivo | O que é |
|---|---|
| `exemplo_pandas_csv.py` | Exemplo do professor. Recorte de Santa Catarina em 2025: detecção de outliers pelos quartis, quais cidades receberam recursos e quanto cada parlamentar empenhou. |
| `ajeitar-dados.py` | **Minha resposta.** Limpeza completa do dataset e as 9 questões da atividade, cada uma com o seu gráfico. |
| `EmendasParlamentares.csv` | O dataset. ⚠️ **Não versionado** (44 MB) — veja abaixo como obter. |

## 📥 Obtendo o dataset

O CSV tem 44 MB e por isso ficou fora do repositório. Baixe em:

**https://portaldatransparencia.gov.br/download-de-dados/emendas-parlamentares**

Salve o arquivo como `EmendasParlamentares.csv` **dentro desta pasta** — os scripts leem por caminho relativo.

## 🧹 O detalhe da limpeza

Esse é o ponto que mais trava iniciantes. O CSV usa:

* **Encoding** `iso-8859-1` (não UTF-8) — sem isso os acentos viram lixo.
* **Separador** `;` (não vírgula) — porque a vírgula já é o separador decimal.
* **Números** no formato `1.234,56` — o ponto é milhar, a vírgula é decimal.

A conversão precisa acontecer nessa ordem:

```python
data[col] = data[col].str.replace('.', '', regex=False)   # tira o separador de milhar
data[col] = data[col].str.replace(',', '.', regex=False)   # vírgula decimal vira ponto
data[col] = pd.to_numeric(data[col], errors='coerce')      # agora sim vira número
```

Inverter os dois primeiros passos destrói o valor: `1.234,56` viraria `1.23456`.

O `errors='coerce'` transforma o que não converter em `NaN` em vez de estourar uma exceção — importante num dataset com dezenas de milhares de linhas onde sempre tem alguma célula vazia.

## ❓ As questões respondidas

| # | Pergunta |
|---|---|
| 1 | Valor total pago por ano |
| 2 | Média e desvio padrão do valor empenhado por região |
| 3 | Top 10 autores de emendas |
| 4 | Número de emendas destinadas a Santa Catarina |
| 5 | Municípios de SC que mais receberam recursos |
| 6 | Emendas com maior diferença entre liquidado e pago |
| 7 | Percentual de restos a pagar cancelados por ano |
| 8 | Subfunção mais comum por região |
| 9 | Linhas sem código IBGE (qualidade do dado) |

## ▶️ Como rodar

```bash
pip install pandas matplotlib

python ajeitar-dados.py
```

Os gráficos abrem em janelas do Matplotlib, uma por questão. Feche cada janela para o script seguir para a próxima.

## 💡 O que eu aprendi aqui

* Dado público brasileiro quase nunca vem pronto para uso — a limpeza é metade do trabalho.
* `groupby()` + `agg()` responde a maioria das perguntas de negócio sem escrever um `for`.
* Desvio padrão alto e média muito acima da mediana são sinal de outliers puxando o resultado. Ver a média sozinha engana.
