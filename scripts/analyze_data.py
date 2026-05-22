import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns


def save_figure(filename):
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()


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
    rq01_lines_stat, rq01_lines_p = calc_mann_whitney('total_lines', 'Tamanho (Linhas)')
    rq01_files_stat, rq01_files_p = calc_mann_whitney('changed_files', 'Tamanho (Arquivos)')
    
    # RQ 02. Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?
    print("\nRQ 02: Tempo de Análise vs Feedback Final")
    rq02_stat, rq02_p = calc_mann_whitney('duration_hours', 'Tempo de Análise (Horas)')
    
    # RQ 03. Qual a relação entre a descrição dos PRs e o feedback final das revisões?
    print("\nRQ 03: Descrição vs Feedback Final")
    rq03_stat, rq03_p = calc_mann_whitney('body_len', 'Tamanho da Descrição (Caracteres)')
    
    # RQ 04. Qual a relação entre as interações nos PRs e o feedback final das revisões?
    print("\nRQ 04: Interações vs Feedback Final")
    rq04_stat, rq04_p = calc_mann_whitney('total_interactions', 'Interações Totais')
    
    print("\n--- B. Número de Revisões ---")
    
    # RQ 05. Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?
    print("\nRQ 05: Tamanho vs Número de Revisões")
    rq05_lines_corr, rq05_lines_p = calc_correlation(df['total_lines'], df['reviews'], 'Tamanho (Linhas)', 'Número de Revisões')
    rq05_files_corr, rq05_files_p = calc_correlation(df['changed_files'], df['reviews'], 'Tamanho (Arquivos)', 'Número de Revisões')
    
    # RQ 06. Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?
    print("\nRQ 06: Tempo de Análise vs Número de Revisões")
    rq06_corr, rq06_p = calc_correlation(df['duration_hours'], df['reviews'], 'Tempo de Análise (Horas)', 'Número de Revisões')
    
    # RQ 07. Qual a relação entre a descrição dos PRs e o número de revisões realizadas?
    print("\nRQ 07: Descrição vs Número de Revisões")
    rq07_corr, rq07_p = calc_correlation(df['body_len'], df['reviews'], 'Tamanho da Descrição (Caracteres)', 'Número de Revisões')
    
    # RQ 08. Qual a relação entre as interações nos PRs e o número de revisões realizadas?
    print("\nRQ 08: Interações vs Número de Revisões")
    rq08_corr, rq08_p = calc_correlation(df['total_interactions'], df['reviews'], 'Interações Totais', 'Número de Revisões')
    
    # Gerar visualizações (barras para RQ01-RQ04 e scatter para RQ05-RQ08)
    print("\nGerando visualizações (RQ01-RQ04 em barras, RQ05-RQ08 em scatter)...")
    sns.set_theme(style="whitegrid")

    merged_color = '#2ca02c'
    closed_color = '#d62728'
    corr_color = '#1f77b4'

    # RQ01 - mediana por status
    rq01_medians = [df_merged['total_lines'].median(), df_closed['total_lines'].median()]
    plt.figure(figsize=(9, 5))
    plt.bar(['MERGED', 'CLOSED'], rq01_medians, color=[merged_color, closed_color])
    plt.yscale('log')
    plt.title('RQ01: Mediana de Tamanho (Linhas) por Status')
    plt.ylabel('Linhas totais (escala log)')
    save_figure('rq01_bar_tamanho_por_status.png')

    # RQ02 - mediana por status
    rq02_medians = [df_merged['duration_hours'].median(), df_closed['duration_hours'].median()]
    plt.figure(figsize=(9, 5))
    plt.bar(['MERGED', 'CLOSED'], rq02_medians, color=[merged_color, closed_color])
    plt.yscale('log')
    plt.title('RQ02: Mediana de Tempo (Horas) por Status')
    plt.ylabel('Duracao em horas (escala log)')
    save_figure('rq02_bar_tempo_por_status.png')

    # RQ03 - mediana por status
    rq03_medians = [df_merged['body_len'].median(), df_closed['body_len'].median()]
    plt.figure(figsize=(9, 5))
    plt.bar(['MERGED', 'CLOSED'], rq03_medians, color=[merged_color, closed_color])
    plt.yscale('symlog')
    plt.title('RQ03: Mediana de Descricao por Status')
    plt.ylabel('Caracteres da descricao (escala symlog)')
    save_figure('rq03_bar_descricao_por_status.png')

    # RQ04 - mediana por status
    rq04_medians = [df_merged['total_interactions'].median(), df_closed['total_interactions'].median()]
    plt.figure(figsize=(9, 5))
    plt.bar(['MERGED', 'CLOSED'], rq04_medians, color=[merged_color, closed_color])
    plt.yscale('log')
    plt.title('RQ04: Mediana de Interacoes por Status')
    plt.ylabel('Interacoes totais (escala log)')
    save_figure('rq04_bar_interacoes_por_status.png')

    # RQ05-RQ08 mantidos no formato original (scatter)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='total_lines', y='reviews', data=df, alpha=0.4)
    plt.xscale('log')
    plt.title('RQ05: Tamanho (Linhas) vs Numero de Revisoes')
    plt.xlabel('Linhas totais (escala log)')
    plt.ylabel('Numero de revisoes')
    save_figure('rq05_tamanho_vs_revisoes.png')

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='duration_hours', y='reviews', data=df, alpha=0.4)
    plt.xscale('log')
    plt.title('RQ06: Tempo de Analise vs Numero de Revisoes')
    plt.xlabel('Duracao em horas (escala log)')
    plt.ylabel('Numero de revisoes')
    save_figure('rq06_tempo_vs_revisoes.png')

    rq07_df = df[df['body_len'] > 0]
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='body_len', y='reviews', data=rq07_df, alpha=0.4)
    plt.xscale('log')
    plt.title('RQ07: Tamanho da Descricao vs Numero de Revisoes')
    plt.xlabel('Caracteres da descricao (escala log)')
    plt.ylabel('Numero de revisoes')
    save_figure('rq07_descricao_vs_revisoes.png')

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='total_interactions', y='reviews', data=df, alpha=0.4)
    plt.xscale('log')
    plt.title('RQ08: Interacoes vs Numero de Revisoes')
    plt.xlabel('Interacoes totais (escala log)')
    plt.ylabel('Numero de revisoes')
    save_figure('rq08_interacoes_vs_revisoes.png')

    print("Análise concluída. RQ01-RQ04 em barras e RQ05-RQ08 no formato original.")

if __name__ == "__main__":
    analyze()
