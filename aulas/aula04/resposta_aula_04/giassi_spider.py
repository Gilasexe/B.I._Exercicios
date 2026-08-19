import scrapy
import w3lib.html

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://www.giassi.com.br/sitemap/product-0.xml",
    ]

    # Mantendo a regra do Erro 404 que você pediu antes
    handle_httpstatus_list = [404]

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set("BOT_NAME", "Pesquisa_Linhas_CFX", priority="spider")
    
    def parse(self, response: scrapy.http.Response):
        response.selector.remove_namespaces()
        
        # Pega todos os links do sitemap do Giassi
        horarios = response.xpath('//loc/text()').getall()
        
        print(f'🚀 Iniciando a raspagem de {len(horarios)} links...')
        
        for url in horarios:
            if url is not None:
                # Usando o response.follow puro do professor (sem meta/playwright)
                yield response.follow(url, self.parse_details)

    def parse_details(self, response: scrapy.http.Response):
        # Tratamento do Erro 404
        if response.status == 404:
            yield {
                'produto': 'Não foi possivel encontrar pois deu erro 404',
                'preco_atual': 'Erro 404',
                'url': response.url,
            }
            print(f"❌ ERRO 404: {response.url}")
            return

        response.selector.remove_namespaces()
        
        # No HTML cru (sem JS), a tag <title> é a forma mais segura de pegar o nome
        line = response.xpath('//title/text()').get()
        
        # E-commerces geralmente deixam o preço escondido em tags <meta> para o Google ler
        preco_meta = response.xpath('//meta[@property="product:price:amount"]/@content').get()
        
        # Limpeza usando a biblioteca w3lib do professor
        nome_limpo = w3lib.html.remove_tags(line).replace('\u00a0','-') if line else "Sem Nome"
        
        # Formata o preço se ele encontrou na tag meta
        preco_final = f"R$ {preco_meta.replace('.', ',')}" if preco_meta else "Preço não encontrado no HTML"

        # Dicionário de saída com os nomes corretos
        lineSchedule = {
            'produto': nome_limpo,
            'preco_atual': preco_final,
            'url': response.url,
        }

        print(f"✅ {nome_limpo} | {preco_final}")

        yield lineSchedule

# --- BLOCO DE EXECUÇÃO ---
if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    import os

    # Avisa o Scrapy que o nosso arquivo de configuração se chama "settings.py" 
    # e está na mesma pasta
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'settings')

    # Agora sim, ele puxa as configurações direto do arquivo!
    process = CrawlerProcess(get_project_settings())
    process.crawl(QuotesSpider)
    process.start()