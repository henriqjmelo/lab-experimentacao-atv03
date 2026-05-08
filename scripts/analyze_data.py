import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def analyze():
    print("Carregando dados...")
    try:
        df = pd.read_csv('github_prs_data.csv')
    except FileNotFoundError:
        print("Arquivo de dados não encontrado. A coleta pode não ter terminado.")
        return
        
    print(f"Total de PRs carregados: {len(df)}")
    
    # Limpeza e preparação dos dados
    df['total_lines'] = df['additions'] + df['deletions']
    df['total_interactions'] = df['participants'] + df['comments']
    
    # Separar em grupos por status
    df_merged = df[df['state'] == 'MERGED']
    df_closed = df[df['state'] == 'CLOSED']
    
    print(f"PRs Merged: {len(df_merged)}")
    print(f"PRs Closed (não merged): {len(df_closed)}")
    
    # Função auxiliar para correlação de Spearman
    def calc_correlation(x, y, label_x, label_y):
        corr, p_value = stats.spearmanr(x, y)
        print(f"Correlação de Spearman entre {label_x} e {label_y}: {corr:.4f} (p-value: {p_value:.4f})")
        return corr, p_value
        
    # Função auxiliar para teste Mann-Whitney U (para comparar Merged vs Closed)
    def calc_mann_whitney(metric, label):
        stat, p_value = stats.mannwhitneyu(df_merged[metric], df_closed[metric], alternative='two-sided')
        print(f"Teste Mann-Whitney U para {label} (Merged vs Closed): stat={stat:.2f}, p-value={p_value:.4f}")
        print(f"Mediana Merged: {df_merged[metric].median():.2f}, Mediana Closed: {df_closed[metric].median():.2f}")
        return stat, p_value
        
    print("\n--- A. Feedback Final das Revisões (Status do PR) ---")
    
    # RQ 01. Qual a relação entre o tamanho dos PRs e o feedback final das revisões?
    print("\nRQ 01: Tamanho vs Feedback Final")
    calc_mann_whitney('total_lines', 'Tamanho (Linhas)')
    calc_mann_whitney('changed_files', 'Tamanho (Arquivos)')
    
    # RQ 02. Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?
    print("\nRQ 02: Tempo de Análise vs Feedback Final")
    calc_mann_whitney('duration_hours', 'Tempo de Análise (Horas)')
    
    # RQ 03. Qual a relação entre a descrição dos PRs e o feedback final das revisões?
    print("\nRQ 03: Descrição vs Feedback Final")
    calc_mann_whitney('body_len', 'Tamanho da Descrição (Caracteres)')
    
    # RQ 04. Qual a relação entre as interações nos PRs e o feedback final das revisões?
    print("\nRQ 04: Interações vs Feedback Final")
    calc_mann_whitney('total_interactions', 'Interações Totais')
    
    print("\n--- B. Número de Revisões ---")
    
    # RQ 05. Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?
    print("\nRQ 05: Tamanho vs Número de Revisões")
    calc_correlation(df['total_lines'], df['reviews'], 'Tamanho (Linhas)', 'Número de Revisões')
    calc_correlation(df['changed_files'], df['reviews'], 'Tamanho (Arquivos)', 'Número de Revisões')
    
    # RQ 06. Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?
    print("\nRQ 06: Tempo de Análise vs Número de Revisões")
    calc_correlation(df['duration_hours'], df['reviews'], 'Tempo de Análise (Horas)', 'Número de Revisões')
    
    # RQ 07. Qual a relação entre a descrição dos PRs e o número de revisões realizadas?
    print("\nRQ 07: Descrição vs Número de Revisões")
    calc_correlation(df['body_len'], df['reviews'], 'Tamanho da Descrição (Caracteres)', 'Número de Revisões')
    
    # RQ 08. Qual a relação entre as interações nos PRs e o número de revisões realizadas?
    print("\nRQ 08: Interações vs Número de Revisões")
    calc_correlation(df['total_interactions'], df['reviews'], 'Interações Totais', 'Número de Revisões')
    
    # Gerar visualizações
    print("\nGerando visualizações...")
    sns.set_theme(style="whitegrid")
    
    # Boxplots para RQ 01-04
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    sns.boxplot(x='state', y='total_lines', data=df, ax=axes[0, 0])
    axes[0, 0].set_yscale('log')
    axes[0, 0].set_title('RQ 01: Tamanho do PR (Linhas) por Status')
    
    sns.boxplot(x='state', y='duration_hours', data=df, ax=axes[0, 1])
    axes[0, 1].set_yscale('log')
    axes[0, 1].set_title('RQ 02: Tempo de Análise (Horas) por Status')
    
    sns.boxplot(x='state', y='body_len', data=df, ax=axes[1, 0])
    axes[1, 0].set_yscale('symlog')
    axes[1, 0].set_title('RQ 03: Tamanho da Descrição por Status')
    
    sns.boxplot(x='state', y='total_interactions', data=df, ax=axes[1, 1])
    axes[1, 1].set_yscale('log')
    axes[1, 1].set_title('RQ 04: Interações Totais por Status')
    
    plt.tight_layout()
    plt.savefig('status_analysis.png')
    
    # Scatter plots para RQ 05-08
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    sns.scatterplot(x='total_lines', y='reviews', data=df, alpha=0.5, ax=axes[0, 0])
    axes[0, 0].set_xscale('log')
    axes[0, 0].set_title('RQ 05: Tamanho (Linhas) vs Revisões')
    
    sns.scatterplot(x='duration_hours', y='reviews', data=df, alpha=0.5, ax=axes[0, 1])
    axes[0, 1].set_xscale('log')
    axes[0, 1].set_title('RQ 06: Tempo de Análise vs Revisões')
    
    sns.scatterplot(x='body_len', y='reviews', data=df, alpha=0.5, ax=axes[1, 0])
    axes[1, 0].set_xscale('symlog')
    axes[1, 0].set_title('RQ 07: Tamanho da Descrição vs Revisões')
    
    sns.scatterplot(x='total_interactions', y='reviews', data=df, alpha=0.5, ax=axes[1, 1])
    axes[1, 1].set_xscale('log')
    axes[1, 1].set_title('RQ 08: Interações vs Revisões')
    
    plt.tight_layout()
    plt.savefig('reviews_analysis.png')
    
    print("Análise concluída e gráficos salvos.")

if __name__ == "__main__":
    analyze()
