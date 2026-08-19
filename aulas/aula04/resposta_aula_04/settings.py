# O nome camuflado que o professor utilizou
BOT_NAME = 'Pesquisa_Linhas_CFX'

# --- CONFIGURAÇÕES ESSENCIAIS PARA O SEU PROJETO ---

# 1. Garante que os acentos (ã, ç) e o símbolo do "R$" saem perfeitos no JSON
FEED_EXPORT_ENCODING = 'utf-8'

# 2. Ignora o ficheiro robots.txt do supermercado para evitar que o bot seja bloqueado
ROBOTSTXT_OBEY = False

# 3. Limite de velocidade. Como o Scrapy puro é muito rápido, 4 páginas em simultâneo é seguro.
CONCURRENT_REQUESTS = 4

# 4. Salva o ficheiro automaticamente com o nome que escolheu
FEEDS = {
    "precos_giassi.json": {"format": "json", "overwrite": True},
}