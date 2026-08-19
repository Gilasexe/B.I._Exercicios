import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

import pca

#Parser dos argumentos de linha de comando
parser = argparse.ArgumentParser("")
parser.add_argument("--vh",required=False, help='Gera visualização da matriz de covariância em formato de heatmap', action='store_true')
parser.add_argument("--vs",required=False,help='Gera visualização da matriz de covariância em formato de graficos de dispersão', action='store_true')

args = parser.parse_args()

print(args)

data = pd.read_csv('notas_sinteticas.csv')
#Calc 1,Álg.Linear,Est.Dados,Bnc.Dados 1,Eng.Softw.,PJA 1
#Carga horária de cada UC
ch_uc = [72,72,72,72,72,40]
#Carga horária total do semestre
ch_semestre = 72 * 5 + 40

#Coeficiente de rendimento: Soma ponderada da nota da UC pela CH / CH_semestre
data['CR'] = (data.mul(ch_uc).sum(axis=1)) / ch_semestre
print(data)

# Padronização (normalização z-score)
data_std = (data - data.mean()) / data.std()  
print(data_std)

# Relação entre as variáveis (notas) do dataset
matriz_covariancia = data_std.cov()

if args.vh:
    # Visualização da matriz de covariância no formato de heatmap
    plt.figure()
    sns.heatmap(matriz_covariancia, annot=True, fmt='.3f', cmap='coolwarm',square=True)
    plt.title("Matriz de Covariância")
    plt.show()
    plt.close()
    
if args.vs:
    plt.figure()
    # Visualização da matriz de covariança em gráficos de dispersão
    pd.plotting.scatter_matrix(matriz_covariancia)
    plt.show()
    plt.close()

componentes, variancia_explicada = pca.pca_svd(data)
print(componentes)

reduzido = pca.aplica_pca(data_std, componentes, 2)
print(reduzido)
plt.figure()
plt.scatter(reduzido[0], reduzido[1])
plt.show()

# Primeiro componente principal é a primeira coluna
cp1 = componentes[:, 0] 
# Primeiro componente principal é a primeira coluna
cp2 = componentes[:, 1] 

# Me diz o quanto cada unidade impacta no componente
importancia_absoluta_cp1 = np.abs(cp1)
importancia_absoluta_cp2 = np.abs(cp2)

cols = data.columns

df_importancia = pd.DataFrame({
    'Feature Original': cols,
    'Peso Real (Loading)': cp1,
    'Importância Absoluta': importancia_absoluta_cp1 
})

df_importancia = df_importancia.sort_values(by='Importância Absoluta', ascending=False)

df_importancia2 = pd.DataFrame({
    'Feature Original': cols,
    'Peso Real (Loading)': cp2,
    'Importância Absoluta': importancia_absoluta_cp2 
})

df_importancia2 = df_importancia2.sort_values(by='Importância Absoluta', ascending=False)