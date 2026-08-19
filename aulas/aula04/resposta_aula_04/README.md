# 🛒 Exercício extra — Raspando preços do Giassi

> Mesmo spider da Aula 04, alvo diferente: um e-commerce de supermercado em vez de horários de ônibus.

## 🎯 O objetivo

Provar que a técnica da aula é genérica. Trocando o sitemap e os seletores, o mesmo esqueleto de spider extrai **nome e preço de produtos** do Giassi Supermercados.

Esse exercício é a base do que vira a [Aula 05](../../aula05), onde os preços coletados alimentam um banco de dados e um relatório de inflação.

## 🔍 O truque: preço na tag `<meta>`

E-commerces renderizam preço via JavaScript, então o HTML cru que o Scrapy recebe geralmente vem **sem** o valor na tela. Só que esses mesmos sites precisam que o Google leia o preço para aparecer bem nas buscas — e por isso deixam o dado exposto em metatags do Open Graph:

```python
preco_meta = response.xpath('//meta[@property="product:price:amount"]/@content').get()
```

Isso evita ter que subir um navegador headless (Playwright) só para ler um número. É mais rápido, mais leve e muito menos frágil.

Pela mesma lógica, o nome do produto sai do `<title>` da página, que também é preenchido no servidor:

```python
line = response.xpath('//title/text()').get()
```

## 🚧 Lidando com 404

O sitemap lista produtos que já saíram do catálogo. Por padrão o Scrapy descarta respostas 404 em silêncio, e você nunca fica sabendo quantos links morreram.

```python
handle_httpstatus_list = [404]
```

Com isso o 404 chega ao `parse_details`, e o spider registra explicitamente o produto como indisponível em vez de simplesmente sumir com ele. Dado ausente que você **sabe** que está ausente vale muito mais do que dado que sumiu sem aviso.

## 📁 Arquivos

| Arquivo | O que é |
|---|---|
| `giassi_spider.py` | O spider. Percorre `sitemap/product-0.xml` e extrai produto, preço e URL. |
| `settings.py` | Configuração do Scrapy usada pelo bloco de execução. |
| `precos_giassi.json` | Saída da coleta. |

## ▶️ Como rodar

```bash
pip install scrapy w3lib

python giassi_spider.py
```

O spider se auto-executa pelo bloco `if __name__ == "__main__"`, que aponta o `SCRAPY_SETTINGS_MODULE` para o `settings.py` desta pasta. Ou seja: não precisa criar um projeto Scrapy completo, é só rodar o arquivo.

## ⚠️ Sobre a qualidade da saída

Olhando o `precos_giassi.json` dá para ver as limitações da abordagem:

* Alguns produtos vêm com `"Preço não encontrado no HTML"` — nem toda página tem a metatag.
* O nome carrega sujeira do template do site (`- giassi - Giassi Supermercados`).

Esses dois problemas são exatamente o que a Aula 05 resolve, com filtros de limpeza na consulta SQL e regras de categorização.
