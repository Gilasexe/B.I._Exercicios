import pandas as pd
import matplotlib.pyplot as plt

# ============================
# 1 - CARREGAR O DATASET
# ============================

data = pd.read_csv("EmendasParlamentares.csv", encoding="iso-8859-1", sep=';', low_memory=False)

# ============================
# 2 - LIMPEZA DOS DADOS
# ============================

colunas_valor = [
    'Valor Empenhado',
    'Valor Liquidado',
    'Valor Pago',
    'Valor Restos A Pagar Cancelados'
]

for col in colunas_valor:
    data[col] = data[col].astype(str)
    data[col] = data[col].str.replace('.', '', regex=False)
    data[col] = data[col].str.replace(',', '.', regex=False)
    data[col] = pd.to_numeric(data[col], errors='coerce')

pd.options.display.float_format = '{:,.2f}'.format

# ============================
# QUESTÃO 1
# Valor total pago por ano
# ============================

valor_pago_ano = data.groupby('Ano da Emenda')['Valor Pago'].sum()

print("\nQUESTÃO 1 - Valor pago por ano")
print(valor_pago_ano)

plt.figure()
valor_pago_ano.plot(kind='bar')
plt.title("Valor total pago por ano")
plt.ylabel("Valor Pago")
plt.xlabel("Ano")
plt.show()

# ============================
# QUESTÃO 2
# Média e desvio padrão por região
# ============================

estat_regiao = data.groupby('Região')['Valor Empenhado'].agg(['mean','std'])

print("\nQUESTÃO 2 - Média e desvio padrão por região")
print(estat_regiao)

plt.figure()
estat_regiao['mean'].plot(kind='bar')
plt.title("Média de valor empenhado por região")
plt.ylabel("Valor médio")
plt.show()

# ============================
# QUESTÃO 3
# Top 10 autores que mais empenharam
# ============================

top_autores = data.groupby('Nome do Autor da Emenda')['Valor Empenhado'].sum()

top10 = top_autores.sort_values(ascending=False).head(10)

print("\nQUESTÃO 3 - Top 10 autores")
print(top10)

plt.figure()
top10.plot(kind='bar')
plt.title("Top 10 autores que mais destinaram recursos")
plt.ylabel("Valor empenhado")
plt.show()

# ============================
# QUESTÃO 4
# Quantas emendas foram para SC
# ============================

emendas_sc = data[data['UF'] == 'SANTA CATARINA']

print("\nQUESTÃO 4 - Número de emendas para SC")
print(len(emendas_sc))

# ============================
# QUESTÃO 5
# Municípios que mais receberam em SC
# ============================

municipios_sc = emendas_sc.groupby('Município')['Valor Empenhado'].sum()

municipios_top = municipios_sc.sort_values(ascending=False).head(10)

print("\nQUESTÃO 5 - Municípios que mais receberam recursos em SC")
print(municipios_top)

plt.figure()
municipios_top.plot(kind='bar')
plt.title("Municípios de SC que mais receberam emendas")
plt.ylabel("Valor empenhado")
plt.show()

# ============================
# QUESTÃO 6
# Diferença entre valor liquidado e pago
# ============================

diferenca = data[abs(data['Valor Liquidado'] - data['Valor Pago']) > 1000000]

print("\nQUESTÃO 6 - Emendas com diferença grande entre liquidado e pago")
print(diferenca[['Valor Liquidado','Valor Pago']].head())

print("Quantidade encontrada:", len(diferenca))

# ============================
# QUESTÃO 7
# Percentual de restos a pagar cancelados
# ============================

dados_ano = data.groupby('Ano da Emenda').agg({
    'Valor Restos A Pagar Cancelados':'sum',
    'Valor Empenhado':'sum'
})

percentual = (dados_ano['Valor Restos A Pagar Cancelados'] / dados_ano['Valor Empenhado']) * 100

print("\nQUESTÃO 7 - Percentual de restos cancelados por ano")
print(percentual)

plt.figure()
percentual.plot()
plt.title("Percentual de restos a pagar cancelados por ano")
plt.ylabel("%")
plt.xlabel("Ano")
plt.show()

# ============================
# QUESTÃO 8
# Subfunção mais comum por região
# ============================

subfuncao = data.groupby(['Região','Nome Subfunção']).size()

subfuncao = subfuncao.reset_index(name='Quantidade')

subfuncao_top = subfuncao.sort_values(['Região','Quantidade'], ascending=[True,False])

print("\nQUESTÃO 8 - Subfunção mais comum por região")
print(subfuncao_top.groupby('Região').head(1))

# ============================
# QUESTÃO 9
# Código IBGE ausente
# ============================

faltando_ibge = data['Código Município IBGE'].isna().sum()

print("\nQUESTÃO 9 - Linhas sem código IBGE")
print(faltando_ibge)

# ============================
# QUESTÃO 10
# Municípios duplicados
# ============================

municipios = data['Município'].value_counts()

print("\nQUESTÃO 10 - Municípios mais frequentes")
print(municipios.head(10))