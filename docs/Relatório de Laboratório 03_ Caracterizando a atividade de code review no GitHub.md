# Relatório de Laboratório 03: Caracterizando a atividade de code review no GitHub

**Curso:** Engenharia de Software  
**Disciplina:** Laboratório de Experimentação de Software  
**Professor:** Danilo de Quadros Maia  

---

## 1. Introdução e Hipóteses

Este relatório apresenta uma análise quantitativa da atividade de code review em repositórios populares do GitHub. O objetivo é identificar variáveis que influenciam o merge de um Pull Request (PR) e o número de revisões realizadas. A pesquisa busca compreender como fatores relacionados ao desenvolvimento colaborativo, como quantidade de comentários, tempo de resposta, tamanho das alterações e participação dos revisores, impactam o processo de aprovação de contribuições em projetos de software de grande escala. 

Além disso, o estudo pretende analisar padrões de comportamento em equipes distribuídas, avaliando de que forma a dinâmica de revisão pode contribuir para a qualidade do código, manutenção do projeto e eficiência no fluxo de desenvolvimento.

### Hipóteses Iniciais
1. **Tamanho do PR:** PRs menores têm maior probabilidade de serem aceitos (merged) e requerem menos revisões.
2. **Tempo de Análise:** PRs que levam mais tempo para serem analisados têm maior chance de serem rejeitados (closed sem merge).
3. **Descrição:** PRs com descrições mais detalhadas facilitam a revisão e são aceitos mais rapidamente.
4. **Interações:** Um maior número de interações (comentários/participantes) indica uma revisão mais rigorosa, possivelmente resultando em mais revisões.

---

## 2. Metodologia

### Coleta de Dados
Os dados foram coletados utilizando a API GraphQL do GitHub. O recorte final contém 200 repositórios (199 com PRs válidos no arquivo final) e 631.440 Pull Requests. Foram considerados os seguintes critérios:
- Status: **MERGED** ou **CLOSED**.
- Repositórios com pelo menos **100 PRs totais** (MERGED + CLOSED) no momento da seleção.
- Pelo menos **uma revisão** realizada (comentários de revisão).
- Intervalo entre criação e fechamento de pelo menos **uma hora**.

### Métricas Definidas
| Métrica | Descrição |
|---------|-----------|
| **Tamanho** | Número total de linhas (adições + remoções) e número de arquivos alterados. |
| **Tempo de Análise** | Intervalo em horas entre a criação do PR e seu fechamento/merge. |
| **Descrição** | Quantidade de caracteres no corpo da descrição do PR. |
| **Interações** | Soma do número de participantes e comentários totais. |

### Testes Estatísticos
- **Mann-Whitney U:** Utilizado para comparar as distribuições entre PRs Merged e Closed, pois os dados não seguem uma distribuição normal.
- **Correlação de Spearman:** Utilizada para medir a força da relação entre as métricas e o número de revisões.

---

## 3. Resultados

### A. Feedback Final das Revisões (Status do PR)

| Questão de Pesquisa | Métrica | Mediana Merged | Mediana Closed | p-value (MWU) | Interpretação
|---------------------|---------|----------------|----------------|---------------|
| **RQ 01: Tamanho** | Linhas | 39,00 | 47,00 | < 0.0001 | PRs merged tendem a ser menores que PRs closed, com diferença significativa.
| **RQ 02: Tempo** | Horas | 28,35 | 233,82 | < 0.0001 | PRs closed permanecem abertos por muito mais tempo, com diferença significativa.
| **RQ 03: Descrição**| Caracteres| 327,00 | 648,00 | < 0.0001 | PRs closed tendem a ter descrições mais longas na mediana.
| **RQ 04: Interações**| Total | 5,00 | 6,00 | < 0.0001 | PRs closed apresentam mais interações na mediana.

### B. Número de Revisões

| Questão de Pesquisa | Variável | Correlação (Spearman) | p-value | Interpretação
|---------------------|----------|-----------------------|---------|
| **RQ 05: Tamanho** | Linhas Totais | 0.3428 | < 0.0001 | Correlação positiva moderada: PRs maiores tendem a ter mais revisões.
| **RQ 06: Tempo** | Duração (h) | 0.2979 | < 0.0001 | Correlação positiva fraca/moderada: PRs com mais revisões tendem a permanecer abertos por mais tempo.
| **RQ 07: Descrição**| Tamanho Descrição| 0.1389 | < 0.0001 | Correlação positiva fraca, porém significativa.
| **RQ 08: Interações**| Interações Totais| 0.4147 | < 0.0001 | Correlação positiva moderada: mais interações se associam a mais revisões.

---

## 4. Discussão

### Análise dos Resultados vs. Hipóteses

1.  **RQ 01 & RQ 02 (Tamanho e Tempo):** PRs merged tendem a ser menores e com menor duração que PRs closed, com diferença estatística clara.
2.  **RQ 03 & RQ 04 (Descrição e Interações):** Na base atual, PRs closed apresentam medianas maiores de descrição e interações.
3.  **RQ 05-RQ08 (Revisões):** Todas as variáveis analisadas apresentam correlação positiva e significativa com o número de revisões, com maior intensidade para interações e tamanho.
4.  **Magnitude dos efeitos:** apesar da significância estatística elevada (N grande), os coeficientes de correlação variam de fracos a moderados, sem evidência de relação forte.

---

## 5. Conclusão

A atividade de code review no GitHub, na base final coletada, mostra diferenças consistentes entre PRs merged e closed em todas as dimensões analisadas (tamanho, tempo, descrição e interações). Em especial, PRs merged tendem a ser menores e concluídos mais rapidamente.

Também foi observada associação positiva entre número de revisões e todas as variáveis estudadas, com maior intensidade para interações e tamanho do PR. Isso reforça que mudanças maiores e discussões mais intensas tendem a demandar mais ciclos de revisão.

Como o volume amostral é muito alto, recomenda-se interpretar significância estatística junto com tamanho de efeito. Os achados são consistentes para orientar práticas de engenharia, como reduzir escopo de PRs e favorecer revisões incrementais.

---

