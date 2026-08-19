import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

def extrair_relatorios():
    print("Conectando ao banco de dados e extraindo informações...\n")
    conn = sqlite3.connect('dados_cesta_basica.db')

    # 1. Consulta SQL para extrair os produtos já limpando os intrusos
    query_produtos = """
    SELECT c.nome as categoria, p.nome_marca, p.preco_unitario, p.medida_unidade
    FROM produtos p
    JOIN categorias c ON p.categoria_id = c.id
    WHERE p.nome_marca NOT LIKE '%Margarina%' 
      AND p.nome_marca NOT LIKE '%Tempero%'
      AND p.nome_marca NOT LIKE '%Aji-Sal%'
      AND p.nome_marca NOT LIKE '%Glúten%'
      AND p.nome_marca NOT LIKE '%Centeio%'
      AND p.nome_marca NOT LIKE '%Bolo%'
      AND p.nome_marca NOT LIKE '%Láctea%'
      AND p.nome_marca NOT LIKE '%Gato%'
      AND p.nome_marca NOT LIKE '%Salmão%'
    """
    df_produtos = pd.read_sql_query(query_produtos, conn)

    # 2. Definindo a quantidade de itens para bater o peso exigido 
    # O Arroz exigido é 5kg (1 pacote de 5kg), Feijão 2kg (2 pacotes de 1kg ou 1 de 2kg), etc.
    def calcular_quantidade(linha):
        cat = linha['categoria']
        nome = linha['nome_marca'].lower()
        if cat == 'feijao' and '1kg' in nome: return 2
        return 1 # Para o resto, assumimos que o scraper pegou a embalagem na medida certa pelas nossas regras
        
    df_produtos['qtd_necessaria'] = df_produtos.apply(calcular_quantidade, axis=1)
    df_produtos['preco_total_item'] = df_produtos['preco_unitario'] * df_produtos['qtd_necessaria']

    # 3. Separando as Cestas (Menor e Maior Valor)
    idx_min = df_produtos.groupby('categoria')['preco_total_item'].idxmin()
    idx_max = df_produtos.groupby('categoria')['preco_total_item'].idxmax()

    cesta_barata = df_produtos.loc[idx_min].copy()
    cesta_cara = df_produtos.loc[idx_max].copy()

    # Divisão de itens obrigatórios e bônus
    obrigatorios = ['arroz', 'feijao', 'oleo', 'acucar', 'cafe']
    
    def calcular_totais(df_cesta, nome_cesta):
        df_obrig = df_cesta[df_cesta['categoria'].isin(obrigatorios)]
        df_bonus = df_cesta[~df_cesta['categoria'].isin(obrigatorios)]
        
        total_obrig = df_obrig['preco_total_item'].sum()
        total_com_bonus = total_obrig + df_bonus['preco_total_item'].sum()
        
        print(f"--- COMPOSIÇÃO DA CESTA DE {nome_cesta.upper()} VALOR ---")
        for _, row in df_cesta.iterrows():
            tipo = "OBRIGATÓRIO" if row['categoria'] in obrigatorios else "BÔNUS"
            print(f"[{tipo}] {row['categoria'].capitalize()}: {row['nome_marca']} | {row['qtd_necessaria']} un x R${row['preco_unitario']:.2f} = R${row['preco_total_item']:.2f}")
            
        print(f"\n> Valor da Cesta Básica (Obrigatórios): R$ {total_obrig:.2f}")
        print(f"> Valor da Cesta + Complemento (Bônus): R$ {total_com_bonus:.2f}\n")
        
        return total_com_bonus

    total_barata = calcular_totais(cesta_barata, "Menor")
    total_cara = calcular_totais(cesta_cara, "Maior")

    # 4. Cálculo da Deflação com IPCA Histórico
    query_ipca = """
    SELECT strftime('%Y', data_referencia) as ano, valor_mensal 
    FROM ipca_historico
    WHERE data_referencia >= '2020-01-01'
    """
    df_ipca = pd.read_sql_query(query_ipca, conn)
    
    # Lógica de juros sobre juros: (1 + i) * (1 + i)... 
    df_ipca['fator_mensal'] = 1 + (df_ipca['valor_mensal'] / 100)
    ipca_anual = df_ipca.groupby('ano')['fator_mensal'].prod() - 1

    print("--- ESTIMATIVA DE VALOR NOS ANOS ANTERIORES (DEFLAÇÃO) ---")
    anos = sorted(ipca_anual.index.tolist(), reverse=True)
    
    # Começamos com o preço de hoje (2026)
    preco_estimado_barata = total_barata
    preco_estimado_cara = total_cara
    
    for ano in anos:
        if ano == '2026': continue # O preço de 2026 é o atual
        
        # Pega a inflação acumulada do ano seguinte para deflacionar o preço
        taxa_ipca_ano_seguinte = ipca_anual[str(int(ano) + 1)]
        
        # Aplica a deflação
        preco_estimado_barata = preco_estimado_barata / (1 + taxa_ipca_ano_seguinte)
        preco_estimado_cara = preco_estimado_cara / (1 + taxa_ipca_ano_seguinte)
        
        print(f"Ano: {ano} | IPCA do ano: {ipca_anual[ano]*100:.2f}%")
        print(f"  -> Cesta Barata Estimada: R$ {preco_estimado_barata:.2f}")
        print(f"  -> Cesta Cara Estimada: R$ {preco_estimado_cara:.2f}")
        print("--------------------------------------------------") 
    
# 5. Exportando os dados para algo físico e visual
    print("\nGerando arquivos físicos (Excel e Gráfico PNG)...")
    
    # Gera arquivos Excel bonitões usando o xlsxwriter para ter controle total do estilo
# Função para exportar e formatar o Excel com Linha de Total
    def exportar_excel_bonitao(df, nome_arquivo):
        # Cria o arquivo usando o xlsxwriter
        with pd.ExcelWriter(nome_arquivo, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Cesta_Basica', index=False)
            
            # Acessa a estrutura interna do Excel
            workbook  = writer.book
            worksheet = writer.sheets['Cesta_Basica']
            
            # 1. Criando os estilos visuais
            estilo_cabecalho = workbook.add_format({
                'bold': True,
                'fg_color': '#1F497D', # Fundo azul escuro
                'font_color': 'white', # Letra branca
                'border': 1
            })
            
            estilo_moeda = workbook.add_format({
                'num_format': 'R$ #,##0.00',
                'border': 1
            })
            
            estilo_normal = workbook.add_format({'border': 1})
            
            # Estilos específicos para a linha do Total
            estilo_total_texto = workbook.add_format({
                'bold': True, 
                'align': 'right'
            })
            estilo_total_valor = workbook.add_format({
                'bold': True, 
                'num_format': 'R$ #,##0.00', 
                'fg_color': '#D9D9D9',
                'border': 1
            })

            # 2. Pintando o cabeçalho
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value.replace('_', ' ').upper(), estilo_cabecalho)

            # 3. Ajustando a largura das colunas e aplicando os estilos
            worksheet.set_column('A:A', 15, estilo_normal) # Categoria
            worksheet.set_column('B:B', 60, estilo_normal) # Nome/Marca (mais larga)
            worksheet.set_column('C:C', 18, estilo_moeda)  # Preço Unitário
            worksheet.set_column('D:D', 15, estilo_normal) # Medida
            worksheet.set_column('E:E', 18, estilo_normal) # Qtd Necessária
            worksheet.set_column('F:F', 18, estilo_moeda)  # Preço Total

            # 4. Inserindo a linha de TOTAL dinamicamente
            num_linhas = len(df)
            linha_total = num_linhas + 1 # +1 porque a linha 0 é o cabeçalho
            
            # Escreve "TOTAL:" na coluna E (índice 4)
            worksheet.write(linha_total, 4, 'TOTAL DA CESTA:', estilo_total_texto)
            
            # Escreve a fórmula na coluna F (índice 5). Ex: =SUM(F2:F9)
            formula_soma = f'=SUM(F2:F{num_linhas + 1})'
            worksheet.write_formula(linha_total, 5, formula_soma, estilo_total_valor)
    
    # Chamando a função para gerar os dois relatórios formatados
    exportar_excel_bonitao(cesta_barata, 'relatorio_cesta_menor_valor.xlsx')
    exportar_excel_bonitao(cesta_cara, 'relatorio_cesta_maior_valor.xlsx')
    
    anos_str = [str(a) for a in anos]
    # Reconstruindo a lista de preços estimados para o gráfico
    precos_barata_grafico = [total_barata]
    precos_cara_grafico = [total_cara]
    
    preco_temp_b = total_barata
    preco_temp_c = total_cara
    
    # Recalcula a regressão para preencher as listas do gráfico
    for ano in anos:
        if ano == '2026': continue
        taxa = ipca_anual[str(int(ano) + 1)]
        preco_temp_b = preco_temp_b / (1 + taxa)
        preco_temp_c = preco_temp_c / (1 + taxa)
        precos_barata_grafico.append(preco_temp_b)
        precos_cara_grafico.append(preco_temp_c)

    # Criação do Gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(anos_str, precos_barata_grafico, marker='o', color='green', label='Cesta Menor Valor', linewidth=2)
    plt.plot(anos_str, precos_cara_grafico, marker='o', color='red', label='Cesta Maior Valor', linewidth=2)
    
    plt.title('Estimativa do Preço da Cesta Básica (2020-2026)', fontsize=14, fontweight='bold')
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Valor Estimado (R$)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Inverte o eixo X para mostrar de 2020 a 2026 da esquerda para a direita
    plt.gca().invert_xaxis() 
    
    # Salva o gráfico como imagem
    plt.savefig('grafico_inflacao_cestas.png', dpi=300, bbox_inches='tight')
    print("Sucesso! 'grafico_inflacao_cestas.png' e planilhas xlsx foram salvos na pasta.")
    conn.close()

if __name__ == "__main__":
    extrair_relatorios()