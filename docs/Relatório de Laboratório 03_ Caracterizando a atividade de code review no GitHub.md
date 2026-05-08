# Relatório de Laboratório 03: Caracterizando a atividade de code review no GitHub

**Curso:** Engenharia de Software  
**Disciplina:** Laboratório de Experimentação de Software  
**Professor:** Danilo de Quadros Maia  

---

## 1. Introdução e Hipóteses

Este relatório apresenta uma análise quantitativa da atividade de code review em repositórios populares do GitHub. O objetivo é identificar variáveis que influenciam o merge de um Pull Request (PR) e o número de revisões realizadas.

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

| Questão de Pesquisa | Métrica | Mediana Merged | Mediana Closed | p-value (MWU) |
|---------------------|---------|----------------|----------------|---------------|
| **RQ 01: Tamanho** | Linhas | 105.00 | 138.50 | 0.0123 |
| **RQ 02: Tempo** | Horas | 23.28 | 34.61 | 0.0003 |
| **RQ 03: Descrição**| Caracteres| 301.50 | 285.00 | 0.6438 |
| **RQ 04: Interações**| Total | 61.00 | 63.00 | 0.9223 |

### B. Número de Revisões

| Questão de Pesquisa | Variável | Correlação (Spearman) | p-value |
|---------------------|----------|-----------------------|---------|
| **RQ 05: Tamanho** | Linhas Totais | 0.4466 | < 0.0001 |
| **RQ 06: Tempo** | Duração (h) | 0.2764 | < 0.0001 |
| **RQ 07: Descrição**| Tamanho Descrição| -0.0826 | 0.0649 |
| **RQ 08: Interações**| Interações Totais| 0.9983 | < 0.0001 |

---

## 4. Discussão

### Análise dos Resultados vs. Hipóteses

1.  **RQ 01 & RQ 02 (Tamanho e Tempo):** Confirmou-se que PRs aceitos (Merged) tendem a ser significativamente menores (105 vs 138 linhas) e processados mais rapidamente (23h vs 34h) do que os rejeitados. O p-value baixo (< 0.05) garante confiança estatística nessas observações.
2.  **RQ 03 (Descrição):** A hipótese de que a descrição influencia o merge não foi sustentada estatisticamente (p-value = 0.64), indicando que, nesta amostra, o tamanho da descrição não foi um fator determinante para o sucesso do PR.
3.  **RQ 05 & RQ 06 (Número de Revisões):** Existe uma correlação positiva moderada entre o tamanho do PR e o número de revisões (0.44). Isso sugere que mudanças maiores naturalmente atraem mais escrutínio e ciclos de revisão.
4.  **RQ 08 (Interações):** Observou-se uma correlação quase perfeita (0.99) entre interações e número de revisões. Isso é esperado, dado que cada revisão gera comentários e envolve participantes, tornando-as variáveis altamente dependentes.

---

## 5. Conclusão

A atividade de code review no GitHub é fortemente influenciada pela complexidade da mudança (tamanho). Manter PRs pequenos e concisos não apenas aumenta a probabilidade de aceitação, mas também reduz o tempo de ciclo e o número de revisões necessárias. A descrição, embora importante para o contexto humano, não apresentou impacto estatístico direto no desfecho binário (merge/close) nesta análise.

---
*Este relatório foi gerado como parte das atividades do Laboratório 03.*
