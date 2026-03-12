import pandas as pd
import matplotlib.pyplot as plt

#Documentação https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
data = pd.read_csv("EmendasParlamentares.csv",encoding="iso-8859-1",sep=';')

# Buscando os dados de 2025
dados_2025 = data[data['Ano da Emenda'] == 2025]
# Gerando uma cópia dos dados de 2025 para o estado de SC
emendas_sc_2025 = dados_2025[dados_2025['UF']=='SANTA CATARINA'].copy()

#Se verificamos os dados da série, percebemos que a leitura do csv não converteu os valores em tipo numérico
print(emendas_sc_2025['Valor Empenhado'])

#Tentamos converter diretamente. Importante, os valores fracionados na planilha estão usando , como separador e pandas espera .
emendas_sc_2025['Valor Empenhado'] = emendas_sc_2025['Valor Empenhado'].str.replace(',','.')
emendas_sc_2025['Valor Empenhado'] = pd.to_numeric(emendas_sc_2025['Valor Empenhado'])

# Formatação de floats para simplificar a visualização
pd.options.display.float_format = '{:,.2f}'.format 

#Estatísticas gerais sobre os valores empenhados no ano de 2025, com destino em SC
emendas_sc_2025['Valor Empenhado'].describe()

#Vemos pelo desvio padrão e pelos quartis que o dataset não é balanceado.
#Valores acima do 3º quartil (75%) estão puxando a média pra cima. Quais são esses valores?
media = emendas_sc_2025['Valor Empenhado'].mean()
#Exibe
top3 = (emendas_sc_2025['Valor Empenhado'][emendas_sc_2025['Valor Empenhado'] > media]).sort_values().tail(3)

#Busco as emendas com o índice apresentado
emendas = emendas_sc_2025.loc[top3.index]

#Remove as emendas com valores discrepantes
n_emendas_sc_2025 = emendas_sc_2025.drop(top3.index,axis='index')
n_emendas_sc_2025.describe()

#Quais cidades foram contempladas?
cidades = emendas_sc_2025['Localidade de aplicação do recurso'].unique()

#Quantas emendas foram destinadas para cada cidade?
histog_cidades = emendas_sc_2025['Localidade de aplicação do recurso'].value_counts()

#Qual foi a emenda destinada para Campos Novos - SC?
emendas_sc_2025[emendas_sc_2025['Localidade de aplicação do recurso']=='CAMPOS NOVOS - SC']

#Para cada cidade com recebimento de emendas, quanto foi empenhado?
valor_por_cidade = emendas_sc_2025.groupby('Localidade de aplicação do recurso')['Valor Empenhado'].sum()

#Quanto cada parlamentar empenhou?
valor_por_parlamentar = emendas_sc_2025.groupby('Nome do Autor da Emenda')['Valor Empenhado'].sum()

#Quais parlamentares empenharam valores com destino a SC?
parlamentares = emendas_sc_2025['Nome do Autor da Emenda'].unique()

#Destes parlamentares, quais empenharam valores com destino em outra UF?
tmp = dados_2025.loc[dados_2025['Nome do Autor da Emenda'].isin(parlamentares) & (dados_2025['UF']!='SANTA CATARINA')]

tmp['Valor Empenhado'] = tmp['Valor Empenhado'].str.replace(',','.')
tmp['Valor Empenhado'] = pd.to_numeric(tmp['Valor Empenhado'])
tmp['Valor Empenhado'].describe()

tmp['Nome do Autor da Emenda'].unique()

#Gráfico de dispersão com os valores, 
emendas_sc_2025.sort_values(by='Valor Empenhado')

plt.scatter(y=emendas_sc_2025['Valor Empenhado'], x=range(0,len(emendas_sc_2025['Valor Empenhado'])))
plt.show()
