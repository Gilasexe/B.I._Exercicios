from typing import Tuple

import numpy as np
import pandas as pd

# Implementação de PCA passo a passo para ilustração
# Assume que os dados já foram normalizados com z-score
def pca_manual(data:pd.DataFrame) ->Tuple[np.ndarray, np.ndarray]:
    # rowvar False porque as variáveis estão nas colunas e não nas linhas
    matriz_covariancia = np.cov(data, rowvar=False)
    autovalores, autovetores = np.linalg.eig(matriz_covariancia)
    ordenacao = np.argsort(autovalores)[::-1]

    autovalores_ordenados = autovalores[ordenacao]
    autovetores_ordenados = autovetores[:, ordenacao]
    variacao_explicada = autovalores_ordenados / np.sum(autovalores_ordenados)
    
    return autovetores_ordenados, variacao_explicada

# Implementação do PCA via decomposição de vetores SVD (Singular Value Decomposition)
def pca_svd(data):
    centralizados = data - data.mean(axis=0)
    # https://icd-ufmg.github.io/22-svd-e-pca/
    U, s, Vt = np.linalg.svd(centralizados)
    # S contém os valores singulares. Podem ser transformados nos autovetores
    # com a formula aut = (s ** 2) / (n - 1) onde n é o número de amostras(linhas)
    # Como a variancia explicada é aut/sum(aut), podemos cancelar a subtração
    # (s**2)/(n-1) / sum((s**2)/(n-1)) = (s ** 2) / sum(s ** 2)
    variancia_explicada = (s ** 2) / np.sum(s ** 2)
    # Retorno a transposta para padronizar os componentes como COLUNAS da matriz
    # Só faço isso aqui para poder usar aplica_pca sem modificação
    return Vt.T, variancia_explicada

def aplica_pca(data:pd.DataFrame, autovetores:np.ndarray, n: int):
    centralizados = data - np.mean(data, axis=0)
    return np.matmul(centralizados, autovetores[:,:n] )

