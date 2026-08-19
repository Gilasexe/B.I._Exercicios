import zipfile
import os

def compactar_projeto():
    nome_zip = "entrega_cesta_basica.zip"
    
    # 1. Lista de arquivos soltos
    arquivos_para_zipar = [
        "database_schema.py",
        "instrucoes.txt",
        "api_ipca.py",
        "scraper_giassi.py",
        "relatorio_cesta.py",
        "dados_cesta_basica.db",
        "scrapy_output.log", 
        "requirements.txt"
    ]
    
    # 2. Lista de pastas (adicione os nomes das pastas aqui)
    pastas_para_zipar = ["resultados"] 
    
    print(f"Preparando pra criar o arquivo {nome_zip}...\n")
    
    try:
        with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            
            # Zipando os arquivos soltos
            for arquivo in arquivos_para_zipar:
                if os.path.exists(arquivo):
                    zipf.write(arquivo)
                    print(f"[OK] Arquivo adicionado: {arquivo}")
                else:
                    print(f"[AVISO] O arquivo '{arquivo}' não foi encontrado.")
            
            # Zipando as pastas inteiras
            for pasta in pastas_para_zipar:
                if os.path.exists(pasta):
                    # O os.walk varre todos os subdiretórios e arquivos dentro da pasta
                    for raiz, diretorios, arquivos in os.walk(pasta):
                        for arquivo in arquivos:
                            caminho_completo = os.path.join(raiz, arquivo)
                            zipf.write(caminho_completo)
                    print(f"[OK] Pasta inteira adicionada: {pasta}/")
                else:
                    print(f"[AVISO] A pasta '{pasta}' não foi encontrada.")
                    
        print(f"\nSucesso total! O pacote '{nome_zip}' tá pronto pra entrega.")
    except Exception as e:
        print(f"Deu ruim na hora de zipar: {e}")

if __name__ == "__main__":
    compactar_projeto()