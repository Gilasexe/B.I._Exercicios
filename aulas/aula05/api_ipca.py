import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database_schema import IPCA

def buscar_dados_ipca():
    print("Buscando dados na API do Banco Central...")
    # URL da API do BCB para a série 433 (IPCA - Variação mensal)
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        df = pd.DataFrame(dados)
        
        # Converte a coluna 'data' para o formato Date do Python
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y').dt.date
        # Garante que o valor da inflação seja numérico
        df['valor'] = df['valor'].astype(float)
        
        print(f"Foram encontrados {len(df)} registros de IPCA.")
        return df
    else:
        print(f"Erro ao acessar a API: Status Code {response.status_code}")
        return None

def salvar_ipca_no_banco(df):
    print("Conectando ao banco de dados...")
    engine = create_engine('sqlite:///dados_cesta_basica.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    registros_inseridos = 0
    
    for index, linha in df.iterrows():
        # Verifica se a data já existe no banco para não duplicar
        existe = session.query(IPCA).filter_by(data_referencia=linha['data']).first()
        
        if not existe:
            novo_registro = IPCA(
                data_referencia=linha['data'],
                valor_mensal=linha['valor']
            )
            session.add(novo_registro)
            registros_inseridos += 1
            
    session.commit()
    session.close()
    print(f"Sucesso! {registros_inseridos} novos registros do IPCA foram salvos no banco de dados.")

if __name__ == "__main__":
    df_ipca = buscar_dados_ipca()
    if df_ipca is not None:
        salvar_ipca_no_banco(df_ipca)