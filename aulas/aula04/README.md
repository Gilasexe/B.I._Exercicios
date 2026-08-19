# 🕷️ Aula 04 — Web Scraping com Scrapy

> Quando o dado não está numa planilha pronta, você vai buscar. Aqui o alvo são os horários de ônibus de Florianópolis.

## 🎯 O que essa aula faz

Extrai os **horários e itinerários de todas as linhas** do Consórcio Fênix (transporte público de Florianópolis) e depois usa esses dados para responder uma pergunta prática: *quais ônibus pegar para chegar num evento na SC-401 num fim de semana?*

O fluxo tem duas etapas bem separadas — e essa separação é de propósito:

```
scrape.py  ──▶  dias_horarios.json  ──▶  parse_data.py  ──▶  ranking de linhas
  (coleta)         (dado bruto)            (análise)
```

Separar coleta de análise significa que você raspa o site **uma vez** e depois itera na análise quantas vezes quiser, sem bater no servidor de novo. Isso é educação básica de scraping: não martelar o site alheio.

## 🗺️ A estratégia: começar pelo sitemap

O spider não sai clicando em links aleatórios. Ele começa em `sitemap.xml` — o arquivo que todo site publica listando as suas próprias páginas.

```python
start_urls = ["https://www.consorciofenix.com.br/sitemap.xml"]
```

Depois filtra só o que interessa:

```python
response.selector.remove_namespaces()
horarios = response.xpath('//url/loc[contains(text(),"/horarios/")]/text()')
```

O `remove_namespaces()` é obrigatório aqui. Sitemaps são XML com namespace declarado, e sem remover isso todo XPath retorna vazio — um erro silencioso que custa horas de debug.

## 📁 Arquivos

| Arquivo | O que é |
|---|---|
| `scrape.py` | O spider. Lê o sitemap, segue as páginas de horário e extrai linha, itinerário e tabela de horários. |
| `dias_horarios.json` | Saída do spider. Dado bruto, aninhado, um objeto por linha de ônibus. |
| `parse_data.py` | A análise. Normaliza o JSON e aplica uma heurística de três filtros. |
| `parsed_data_frame.xlsx` | Resultado exportado para Excel. |
| `settings.py` | Configuração do Scrapy com os handlers do Playwright (para páginas que dependem de JavaScript). |
| `sitemap_consorciofenix.xml` | Cópia do sitemap do site, guardada como referência do que o spider enxerga. |
| `resposta_aula_04/` | Exercício extra: o mesmo spider apontado para o supermercado Giassi. |

## 🔍 A heurística do `parse_data.py`

O JSON bruto é aninhado: cada linha tem uma lista de horários, e cada horário tem uma lista de partidas. Para analisar isso em tabela, achatamos em dois passos:

```python
df = pandas.json_normalize(data, record_path=["horarios"], meta=["linha", "itinerario"])
df = df.explode('time')   # uma linha por horário de partida
```

O `meta=[...]` mantém `linha` e `itinerario` repetidos em cada linha nova — sem isso você perde a informação de qual ônibus é qual.

Depois, três filtros em sequência:

1. **Local** — a linha passa pela SC-401 ou pela Rod. Virgílio Várzea?
2. **Dia** — é sábado, domingo ou feriado?
3. **Janela de horário** — a partida está entre 10:00 e 13:00?

O filtro de local tem uma sutileza: cada linha escreve o nome da rua de um jeito diferente (`SC 401`, `SC-401`, `JOSE CARLOS DAUX`). Por isso a busca testa as três grafias, e o itinerário passa antes por `unidecode()` para tirar acentos e normalizar a comparação.

## ▶️ Como rodar

```bash
pip install scrapy w3lib pandas unidecode openpyxl
```

**1. Coletar** (roda o spider standalone, sem precisar criar um projeto Scrapy):

```bash
scrapy runspider scrape.py -o dias_horarios.json
```

**2. Analisar:**

```bash
python parse_data.py
```

A saída no terminal traz o ranking de linhas com mais partidas na janela, e depois o detalhe de cada horário sugerido.

## 💡 O que eu aprendi aqui

* Sitemap é o melhor ponto de entrada para raspar um site inteiro — está lá justamente para ser lido por robôs.
* `remove_namespaces()` em XML, sempre. É a causa número um de XPath que "não funciona".
* Salvar o dado bruto em disco antes de analisar economiza tempo e é mais educado com o servidor.
* Dado do mundo real não tem padrão de escrita. Normalizar texto (`unidecode`, `.strip()`, comparar variações) é parte do trabalho, não um extra.
