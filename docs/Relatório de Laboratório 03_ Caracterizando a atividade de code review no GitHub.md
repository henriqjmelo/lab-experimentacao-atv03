# Relatório de Laboratório 03: Caracterizando a atividade de code review no GitHub

**Curso:** Engenharia de Software  
**Disciplina:** Laboratório de Experimentação de Software  
**Professor:** Danilo de Quadros Maia  

---

## 1. Introdução e Hipóteses

Este relatório apresenta uma análise quantitativa da atividade de code review em repositórios populares do GitHub. O objetivo é investigar variáveis associadas ao desfecho de Pull Requests (MERGED/CLOSED) e ao número de revisões realizadas. Em termos analíticos, busca-se compreender como fatores de complexidade e interação colaborativa, como tamanho das mudanças, tempo de análise, descrição textual e volume de interações, se relacionam com o processo de avaliação de contribuições em projetos de software de larga escala.

O estudo também examina padrões de revisão em ambientes distribuídos, com foco em implicações práticas para qualidade de código, manutenção e eficiência do fluxo de desenvolvimento.

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
- **Mann-Whitney U:** Utilizado para comparar as distribuições entre PRs MERGED e CLOSED, pois os dados não seguem uma distribuição normal.
- **Correlação de Spearman:** Utilizada para medir a força da relação entre as métricas e o número de revisões.

---

## 3. Resultados

### A. Feedback Final das Revisões (Status do PR)

| Questão de Pesquisa | Métrica | Mediana Merged | Mediana Closed | p-value (MWU) | Interpretação
|---------------------|---------|----------------|----------------|---------------|
| **RQ 01: Tamanho** | Linhas | 39,00 | 47,00 | < 0.0001 | PRs MERGED tendem a ser menores que PRs CLOSED, com diferença significativa.
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

1.  **RQ 01 & RQ 02 (Tamanho e Tempo):** PRs MERGED tendem a ser menores e apresentam menor duração que PRs CLOSED, com diferença estatística robusta.
2.  **RQ 03 & RQ 04 (Descrição e Interações):** PRs CLOSED apresentam medianas mais elevadas para descrição e interações totais.
3.  **RQ 05-RQ08 (Revisões):** Todas as variáveis analisadas se associam positivamente ao número de revisões, com maior intensidade para interações e tamanho.
4.  **Magnitude dos efeitos:** apesar da significância estatística elevada (N grande), os coeficientes observados permanecem na faixa fraca a moderada, sem evidência de efeito forte.

---

## 5. Conclusão

Os resultados indicam diferenças sistemáticas entre PRs MERGED e CLOSED em todas as dimensões avaliadas (tamanho, tempo, descrição e interações). De modo geral, PRs MERGED tendem a ser menores e concluídos mais rapidamente.

Observou-se, adicionalmente, associação positiva entre número de revisões e todas as variáveis analisadas, com maior intensidade para interações e tamanho do PR. Esse padrão é compatível com a interpretação de que mudanças mais extensas e discussões mais ativas demandam mais ciclos de revisão.

Considerando o tamanho amostral elevado, a interpretação dos resultados deve combinar significância estatística e magnitude de efeito. Ainda assim, os achados oferecem evidências úteis para práticas de engenharia, como decomposição de mudanças em PRs menores e incentivo a revisões incrementais.

## 6. Limitações

1. O recorte final inclui 200 repositórios na lista consolidada; no entanto, 199 possuem dados válidos no dataset final de PRs.
2. As associações identificadas são de natureza observacional e não devem ser interpretadas como causalidade.

---

