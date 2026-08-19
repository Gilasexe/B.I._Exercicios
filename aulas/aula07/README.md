# 🧮 Aula 07 (EAD) — Feature Engineering e PCA

> Redução de dimensionalidade escrita na mão, sem scikit-learn. Se você entende o que acontece dentro do PCA, você para de tratá-lo como caixa-preta.

## 🎯 O que essa aula faz

Duas frentes:

1. **Implementar PCA do zero** — só NumPy, por dois caminhos diferentes (matriz de covariância e SVD).
2. **Aplicar em dados reais** — os Indicadores de Desenvolvimento Mundial (WDI) do Banco Mundial, comprimindo 12 indicadores socioeconômicos em 2 dimensões que dá para plotar.

## 📐 O PCA em duas implementações

O módulo `pca.py` traz as duas rotas para o mesmo destino:

**`pca_manual()`** — o caminho do livro-texto:

```python
matriz_covariancia = np.cov(data, rowvar=False)
autovalores, autovetores = np.linalg.eig(matriz_covariancia)
ordenacao = np.argsort(autovalores)[::-1]
```

Calcula a covariância, extrai autovalores e autovetores, ordena do maior para o menor. O maior autovalor aponta para a direção de maior variância — o Componente Principal 1.

> ⚠️ O `rowvar=False` é essencial: o NumPy assume por padrão que cada **linha** é uma variável, mas em DataFrames as variáveis estão nas **colunas**.

**`pca_svd()`** — o caminho que se usa na prática:

```python
centralizados = data - data.mean(axis=0)
U, s, Vt = np.linalg.svd(centralizados)
variancia_explicada = (s ** 2) / np.sum(s ** 2)
```

A decomposição em valores singulares chega no mesmo resultado sem nunca montar a matriz de covariância — é numericamente mais estável e mais rápido. É o que o scikit-learn faz por baixo do capô.

O comentário no código explica a álgebra: como a variância explicada é uma razão, o fator `1/(n-1)` cancela em cima e embaixo, e sobra só `s² / Σs²`.

## 🌍 A análise do WDI

O notebook `feito/aula_07_ead_feito.ipynb` responde 5 questões sobre o período da pandemia (média de 2019 a 2023), com 12 features cobrindo quatro pilares: econômico, saúde, educação/social e ambiental.

| # | Questão | Técnica |
|---|---|---|
| 1 | O que o PC1 representa de fato? | Leitura dos *loadings* — quais indicadores pesam mais no componente |
| 2 | Índice de Eficiência de Saúde | Feature derivada: expectativa de vida ÷ gasto per capita em saúde |
| 3 | Nível Industrial | Discretização por quartis (Alta / Média / Baixa) para colorir o scatter |
| 4 | Normalização condicional | Consumo total → consumo *per capita*, dividindo pela população |
| 5 | Tratamento de assimetria | `np.log()` no PIB per capita para domar a cauda longa |

### Por que z-score antes do PCA

```python
data_pca_norm = (data_pca - data_pca.mean()) / data_pca.std()
```

Sem padronizar, o PCA fica dominado por quem tem a maior escala numérica. PIB per capita anda na casa dos milhares de dólares; expectativa de vida fica entre 50 e 85. Sem z-score, o PC1 vira "o eixo do PIB" e ignora todo o resto — não porque o PIB explica mais, mas porque o número dele é maior.

### Por que log no PIB

A distribuição de PIB per capita entre países é violentamente assimétrica: uma multidão de países pobres e uma cauda longa de riquíssimos. O logaritmo comprime a cauda e aproxima a distribuição de uma normal, que é o que a maioria dos métodos estatísticos assume.

## 📁 Arquivos

| Arquivo | O que é |
|---|---|
| `pca.py` | **O módulo central.** `pca_manual()`, `pca_svd()` e `aplica_pca()`. |
| `exemplo_notas.py` | Exemplo do professor. PCA em notas sintéticas de UCs, com cálculo de coeficiente de rendimento ponderado pela carga horária. |
| `exemplo_pca_WDIC.ipynb` | Notebook base fornecido na atividade. |
| `feito/aula_07_ead_feito.ipynb` | **Minha resposta.** As 5 questões resolvidas. |
| `notas_sinteticas.csv` | Dataset pequeno do exemplo de notas. |
| `Atividade_ Feature Engineering e PCA.docx.pdf` | Enunciado da atividade. |
| `WDI*.csv` | Datasets do Banco Mundial. ⚠️ **Não versionados** — veja abaixo. |

## 📥 Obtendo os datasets do WDI

Os arquivos do World Development Indicators são pesados demais para o Git — o `WDICSV.csv` sozinho tem **188 MB**, acima do limite de 100 MB por arquivo do GitHub.

Baixe o pacote completo em:

**https://datacatalog.worldbank.org/search/dataset/0037712/World-Development-Indicators**

Extraia nesta pasta. Você vai precisar de:

* `WDICSV.csv` — a série completa, um valor por país/indicador/ano.
* `WDICountry.csv` — dicionário de países (usado para separar países de agregados regionais).
* `WDISeries.csv` — dicionário dos indicadores.

O `WDICSV_preparado.csv` que o notebook lê é uma versão derivada: o `WDICSV.csv` filtrado para 2019–2023 e agregado pela média de cada país/indicador. É gerado a partir do notebook base `exemplo_pca_WDIC.ipynb`.

## ▶️ Como rodar

```bash
pip install numpy pandas matplotlib seaborn jupyter
```

**O exemplo de notas** (leve, roda na hora):

```bash
python exemplo_notas.py --vh    # heatmap da matriz de covariância
python exemplo_notas.py --vs    # matriz de gráficos de dispersão
```

**O notebook do WDI:**

```bash
jupyter notebook feito/aula_07_ead_feito.ipynb
```

> 📌 O notebook faz `import pca`, então precisa enxergar o `pca.py` da pasta pai. Rode-o a partir do diretório `aula07/` ou copie o `pca.py` para junto dele.

## 💡 O que eu aprendi aqui

* PCA não é mágica: é autovetor de matriz de covariância. Escrever na mão desmistifica.
* Padronizar antes é obrigatório, não opcional. Escala diferente = resultado sem sentido.
* Feature engineering é onde está o valor real — razões (eficiência de saúde), normalizações condicionais (per capita) e transformações (log) mudam mais o resultado do que trocar de algoritmo.
* Um componente principal só significa alguma coisa depois que você lê os *loadings* e dá um nome a ele.
