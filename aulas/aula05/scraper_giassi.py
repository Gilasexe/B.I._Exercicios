import scrapy
from scrapy.crawler import CrawlerProcess
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_schema import Produto, Categoria
from datetime import date

# 1. Configuração do Banco de Dados
engine = create_engine('sqlite:///dados_cesta_basica.db')
Session = sessionmaker(bind=engine)
session = Session()

# Lista de categorias (obrigatórias e bônus)
CATEGORIAS_ALVO = [
    "arroz", "feijao", "oleo", "acucar", "cafe", 
    "macarrao", "farinha", "sal"
]

def inicializar_categorias():
    """Garante que as categorias existem no banco antes de rodar o spider"""
    for cat_nome in CATEGORIAS_ALVO:
        cat = session.query(Categoria).filter_by(nome=cat_nome).first()
        if not cat:
            session.add(Categoria(nome=cat_nome))
    session.commit()

# 2. O Spider criado a partir do template do professor
class CestaSpider(scrapy.Spider):
    name = "cesta_basica"
    start_urls = ["https://www.giassi.com.br/sitemap.xml"]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2, 
        'RANDOMIZE_DOWNLOAD_DELAY': True, 
        'CONCURRENT_REQUESTS': 1, 
        'LOG_FILE': 'scrapy_output.log',
        'HTTPCACHE_ENABLED': True, 
        'HTTPCACHE_EXPIRATION_SECS': 86400, 
        'HTTPCACHE_DIR': 'cache',
        'HTTPCACHE_IGNORE_HTTP_CODES': [404, 500, 502, 503]
    }

    def parse(self, response: scrapy.http.Response):
        # Pega os sitemaps referentes aos PRODUTOS
        response.selector.remove_namespaces()
        produtos = response.xpath('//sitemap/loc[contains(text(), "/product")]/text()').getall()
        
        print(f"Encontrados {len(produtos)} sitemaps de produtos.")
        
        for url in produtos:
            if url is not None:
                yield response.follow(url, self.parse_lista_produtos)

    def parse_lista_produtos(self, response: scrapy.http.Response):
        # Busca produtos da cesta básica
        response.selector.remove_namespaces()
        urls_produtos = response.xpath('//url/loc/text()').getall()
        
        # Filtros rigorosos baseados nas quantidades exigidas
        regras_filtro = {
            "arroz": {"include": ["arroz", "5kg"], "exclude": ["bifum", "bolinho", "racao", "caes", "cachorro", "pet"]},
            "feijao": {"include": ["feijao", "2kg"], "exclude": ["fantasia", "doce"]},
            "oleo": {"include": ["oleo", "soja", "900ml"], "exclude": ["cabelo", "corporal", "leave-in", "milagroso", "motor"]},
            "acucar": {"include": ["acucar", "1kg"], "exclude": ["zero", "refrigerante", "mascavo", "demerara", "uniao-sucralose"]},
            "cafe": {"include": ["cafe", "500g"], "exclude": ["copo", "soluvel", "capsula", "filtro", "garrafa"]},
            "macarrao": {"include": ["macarrao", "1kg"], "exclude": ["instantaneo", "cup"]},
            "farinha": {"include": ["farinha", "500g"], "exclude": ["lactea", "rosca", "trigo", "arroz", "tapioca", "aveia"]},
            "sal": {"include": ["sal", "1kg"], "exclude": ["salgadinho", "manteiga", "grosso", "parrilha", "parrilla", "churrasco"]}
        }

        for url in urls_produtos:
            url_lower = url.lower()
            
            for categoria, condicoes in regras_filtro.items():
                # Verifica se TODAS as palavras obrigatórias estão na URL
                tem_tudo = all(palavra in url_lower for palavra in condicoes["include"])
                
                # Verifica se NENHUMA das palavras proibidas está na URL
                tem_excluidos = any(palavra in url_lower for palavra in condicoes["exclude"])
                
                if tem_tudo and not tem_excluidos:
                    yield response.follow(url, self.parse_info_produtos, meta={'categoria': categoria})

    def parse_info_produtos(self, response: scrapy.http.Response):
        # Extrai a informação do produto
        nome_marca = response.css('title::text').get()
        if nome_marca:
            nome_marca = nome_marca.split('|')[0].strip()
            
        # Tentativa de pegar o preço
        preco_texto = response.css('meta[property="product:price:amount"]::attr(content)').get()
        if not preco_texto:
             preco_texto = response.css('.vtex-product-price-1-x-currencyContainer .vtex-product-price-1-x-currencyInteger::text').get()
             
        # Tentativa de pegar a medida
        medida_unidade = "1 un"
        if nome_marca:
            partes_nome = nome_marca.lower()
            if 'kg' in partes_nome: medida_unidade = 'kg'
            elif 'g' in partes_nome: medida_unidade = 'g'
            elif 'ml' in partes_nome: medida_unidade = 'ml'
            elif 'l' in partes_nome: medida_unidade = 'l'

        if nome_marca and preco_texto:
            try:
                preco_float = float(preco_texto.replace(',', '.'))
                categoria_nome = response.meta['categoria']
                
                categoria_db = session.query(Categoria).filter_by(nome=categoria_nome).first()
                
                novo_produto = Produto(
                    categoria_id=categoria_db.id,
                    nome_marca=nome_marca,
                    preco_unitario=preco_float,
                    medida_unidade=medida_unidade,
                    data_coleta=date.today()
                )
                session.add(novo_produto)
                session.commit()
                
                print(f"Salvo: {nome_marca} - R$ {preco_float} ({categoria_nome})")
                
            except Exception as e:
                print(f"Erro ao salvar o produto {nome_marca}: {e}")
                session.rollback()

# 3. Execução do script
if __name__ == "__main__":
    print("Inicializando categorias no banco de dados...")
    inicializar_categorias()
    
    print("Iniciando o Web Scraper. Isso pode demorar um pouco por causa do DOWNLOAD_DELAY...")
    process = CrawlerProcess()
    process.crawl(CestaSpider)
    process.start()
    
    print("Raspagem concluída! Verifique o arquivo dados_cesta_basica.db")