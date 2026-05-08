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
Os dados foram coletados utilizando a API do GitHub (REST v3). Foram selecionados Pull Requests de repositórios populares que atendessem aos seguintes critérios:
- Status: **MERGED** ou **CLOSED**.
- Mínimo de **100 PRs** analisados.
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
| **RQ 01: Tamanho** | Linhas | 105.00 | 138.50 | 0.0123 |PRs menores apresentaram maior taxa de aprovação, indicando que mudanças mais compactas tendem a facilitar o processo de revisão.
| **RQ 02: Tempo** | Horas | 23.28 | 34.61 | 0.0003 | PRs aceitos foram processados mais rapidamente, sugerindo que revisões mais ágeis estão associadas a contribuições mais eficientes.
| **RQ 03: Descrição**| Caracteres| 301.50 | 285.00 | 0.6438 | Não foi encontrada diferença estatisticamente significativa entre PRs aceitos e rejeitados em relação ao tamanho da descrição.
| **RQ 04: Interações**| Total | 61.00 | 63.00 | 0.9223 | O volume de interações não apresentou impacto relevante no resultado final do PR dentro da amostra analisada.

### B. Número de Revisões

| Questão de Pesquisa | Variável | Correlação (Spearman) | p-value | Interpretação
|---------------------|----------|-----------------------|---------|
| **RQ 05: Tamanho** | Linhas Totais | 0.4466 | < 0.0001 | Foi identificada uma correlação positiva moderada entre o tamanho do PR e o número de revisões, indicando que alterações maiores tendem a exigir mais ciclos de análise.
| **RQ 06: Tempo** | Duração (h) | 0.2764 | < 0.0001 | Observou-se uma correlação positiva fraca entre o tempo de processamento e o número de revisões, sugerindo que PRs com revisões mais extensas permanecem abertos por mais tempo.
| **RQ 07: Descrição**| Tamanho Descrição| -0.0826 | 0.0649 | A correlação encontrada foi muito fraca e estatisticamente não significativa, indicando que o tamanho da descrição praticamente não influencia a quantidade de revisões realizadas.
| **RQ 08: Interações**| Interações Totais| 0.9983 | < 0.0001 | Foi observada uma correlação extremamente alta entre interações e número de revisões, demonstrando forte dependência entre comentários, participantes e atividades de revisão.

---

## 4. Discussão

### Análise dos Resultados vs. Hipóteses

1.  **RQ 01 & RQ 02 (Tamanho e Tempo):** Confirmou-se que PRs aceitos (Merged) tendem a ser significativamente menores (105 vs 138 linhas) e processados mais rapidamente (23h vs 34h) do que os rejeitados. O p-value baixo (< 0.05) garante confiança estatística nessas observações.
2.  **RQ 03 (Descrição):** A hipótese de que a descrição influencia o merge não foi sustentada estatisticamente (p-value = 0.64), indicando que, nesta amostra, o tamanho da descrição não foi um fator determinante para o sucesso do PR.
3.  **RQ 05 & RQ 06 (Número de Revisões):** Existe uma correlação positiva moderada entre o tamanho do PR e o número de revisões (0.44). Isso sugere que mudanças maiores naturalmente atraem mais escrutínio e ciclos de revisão.
4.  **RQ 08 (Interações):** Observou-se uma correlação quase perfeita (0.99) entre interações e número de revisões. Isso é esperado, dado que cada revisão gera comentários e envolve participantes, tornando-as variáveis altamente dependentes.

---

## 5. Conclusão

A atividade de code review no GitHub mostrou-se fortemente influenciada pela complexidade das alterações realizadas, especialmente pelo tamanho do Pull Request. Os resultados indicam que PRs menores e mais concisos possuem maior probabilidade de aprovação, além de apresentarem menor tempo de processamento e menos ciclos de revisão. Isso evidencia que mudanças reduzidas facilitam a análise por parte dos revisores, tornando o processo mais eficiente e colaborativo.

Além disso, verificou-se que PRs maiores tendem a gerar mais interações, comentários e revisões, aumentando o esforço necessário para validação e integração do código. Dessa forma, a fragmentação de alterações em contribuições menores pode representar uma estratégia importante para otimizar o fluxo de desenvolvimento e melhorar a produtividade das equipes.

Por outro lado, embora a descrição do PR seja relevante para fornecer contexto aos revisores e facilitar a comunicação entre colaboradores, a análise estatística realizada não identificou impacto direto dessa variável no resultado final de aprovação ou rejeição do PR. Isso sugere que fatores técnicos e estruturais relacionados à própria mudança possuem maior influência no processo de merge do que o tamanho textual da descrição apresentada.

---

