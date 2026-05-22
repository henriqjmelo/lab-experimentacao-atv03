# Lab03S03: Análise de Dados e Visualizações

## Resumo Executivo

Este documento apresenta a análise de 631.440 Pull Requests (PRs) provenientes de um recorte final de 200 repositórios, dos quais 199 possuem dados válidos no dataset de PRs. O objetivo é examinar, de forma quantitativa, a associação entre características dos PRs, o desfecho do processo de revisão (MERGED/CLOSED) e o número de revisões realizadas.

---

## Metodologia de Análise

### 1. Preparação dos Dados

**Dataset:** 631.440 PRs do recorte final de 200 repositórios
- **PRs MERGED:** 495.252 (78,43%)
- **PRs CLOSED:** 136.188 (21,57%)

**Filtros aplicados:**
- Status: MERGED ou CLOSED
- Mínimo de 1 revisão
- Duração ≥ 1 hora (entre criação e fechamento)

### 2. Métricas Calculadas

| Dimensão | Métrica | Descrição |
|----------|---------|-----------|
| **Tamanho** | Linhas Adicionadas | Total de adições no PR |
| | Linhas Removidas | Total de deleções no PR |
| | Arquivos Alterados | Número de arquivos mudados |
| **Tempo de Análise** | Duração (horas) | Intervalo criação → fechamento |
| **Descrição** | Caracteres | Tamanho do corpo descritivo em caracteres |
| **Interações** | Participantes | Número de usuários envolvidos |
| | Comentários | Total de comentários |
| | Revisões | Número total de revisões |

### 3. Testes Estatísticos Utilizados

#### A. Teste U de Mann-Whitney (Questões RQ01-RQ04)

**Aplicação:** Comparação entre dois grupos independentes sob distribuição não normal.

**Hipóteses (RQ01-RQ04):**
- **H₀ (nula):** Não há diferença nas distribuições entre PRs MERGED e CLOSED
- **H₁ (alternativa):** Há diferença significativa entre os grupos

**Interpretação:**
- p-value < 0.05: Rejeita H₀ (diferença significativa)
- p-value ≥ 0.05: Não rejeita H₀ (sem diferença significativa)

**Por que Mann-Whitney U?**
- Os dados não seguem distribuição normal (verificado com histogramas)
- Teste não-paramétrico, robusto para dados assimétricos
- Apropriado para dados ordinais ou contínuos não-normais

#### B. Correlação de Spearman (Questões RQ05-RQ08)

**Aplicação:** Medir associação monotônica entre variáveis contínuas.

**Fórmula:**
$$\rho = 1 - \frac{6\sum d_i^2}{n(n^2-1)}$$

Onde $d_i$ é a diferença de ranks entre pares.

**Valores de interpretação:**
- |ρ| = 0.0-0.3: Correlação fraca
- |ρ| = 0.3-0.7: Correlação moderada
- |ρ| = 0.7-1.0: Correlação forte

**Por que Spearman (não Pearson)?**
- Dados não seguem distribuição normal
- Menos sensível a outliers
- Não assume relação linear (apenas monotônica)
- Mais apropriado para dados com valores extremos

---

## Resultados Principais

### A. Feedback Final das Revisões (Status do PR)

#### RQ 01: Tamanho vs Feedback Final

```
Teste Mann-Whitney U para Tamanho (Linhas)
p-value: < 0.0001
Mediana MERGED: 39 linhas
Mediana CLOSED: 47 linhas
```
**Resultado:** Diferença estatisticamente significativa (p < 0.05)

#### RQ 02: Tempo de Análise vs Feedback Final

```
Teste Mann-Whitney U para Duração
p-value: < 0.0001
Mediana MERGED: 28.35 horas
Mediana CLOSED: 233.82 horas
```
**Resultado:** Diferença estatisticamente significativa (p < 0.05)

#### RQ 03: Descrição vs Feedback Final

```
Teste Mann-Whitney U para Descrição
p-value: < 0.0001
Mediana MERGED: 327 caracteres
Mediana CLOSED: 648 caracteres
```
**Resultado:** Diferença estatisticamente significativa (p < 0.05)

#### RQ 04: Interações vs Feedback Final

```
Teste Mann-Whitney U para Interações
p-value: < 0.0001
Mediana MERGED: 5 interações
Mediana CLOSED: 6 interações
```
**Resultado:** Diferença estatisticamente significativa (p < 0.05)

---

### B. Número de Revisões

#### RQ 05: Tamanho vs Número de Revisões

```
Correlação Spearman (Tamanho em Linhas Totais):
ρ = 0.3428, p-value < 0.0001
```
**Resultado:** Correlação positiva moderada e significativa

#### RQ 06: Tempo de Análise vs Número de Revisões

```
Correlação Spearman:
ρ = 0.2979, p-value < 0.0001
```
**Resultado:** Correlação positiva fraca/moderada e significativa

#### RQ 07: Descrição vs Número de Revisões

```
Correlação Spearman:
ρ = 0.1389, p-value < 0.0001
```
**Resultado:** Correlação positiva fraca e significativa

#### RQ 08: Interações vs Número de Revisões

```
Correlação Spearman:
ρ = 0.4147, p-value < 0.0001
```
**Resultado:** Correlação positiva moderada e significativa

---

## Visualizações Geradas

### 1. docs/rq01_bar_tamanho_por_status.png
RQ01: Mediana de tamanho do PR (linhas) por status (gráfico de barras com escala log).

### 2. docs/rq02_bar_tempo_por_status.png
RQ02: Mediana de tempo de análise (horas) por status (gráfico de barras com escala log).

### 3. docs/rq03_bar_descricao_por_status.png
RQ03: Mediana do tamanho da descrição por status (gráfico de barras com escala symlog).

### 4. docs/rq04_bar_interacoes_por_status.png
RQ04: Mediana de interações totais por status (gráfico de barras com escala log).

### 5. docs/rq05_tamanho_vs_revisoes.png
RQ05: Tamanho (linhas) vs número de revisões (scatter com eixo x em log).

### 6. docs/rq06_tempo_vs_revisoes.png
RQ06: Tempo de análise vs número de revisões (scatter com eixo x em log).

### 7. docs/rq07_descricao_vs_revisoes.png
RQ07: Tamanho da descrição vs número de revisões (scatter com eixo x em log).

### 8. docs/rq08_interacoes_vs_revisoes.png
RQ08: Interações totais vs número de revisões (scatter com eixo x em log).

---

## Conclusões

1. As quatro dimensões analisadas apresentam diferença estatisticamente significativa entre PRs MERGED e CLOSED.
2. Em termos de tendência central, PRs MERGED são, em geral, menores e mais rápidos que PRs CLOSED.
3. PRs CLOSED apresentam medianas superiores para tamanho de descrição e interações totais.
4. O número de revisões está positivamente associado a tamanho, tempo e interações, com magnitudes entre fraca e moderada.
5. A variável descrição também apresenta associação positiva com revisões, porém com efeito de menor intensidade.

## Limitações

1. O recorte final contém 200 repositórios, mas 1 deles não possui linhas no dataset final de PRs, totalizando 199 repositórios com dados válidos para análise efetiva.
2. Devido ao grande tamanho amostral, recomenda-se interpretar significância estatística em conjunto com magnitude de efeito.

---

## Arquivos Gerados

- `github_prs_data.csv` - Dataset completo (631.440 registros)
- `repositorios_selecionados.csv` - Lista de 200 repositórios
- `repositorios_selecionados.json` - Lista em JSON
- `docs/rq01_bar_tamanho_por_status.png` - Visualização da RQ01
- `docs/rq02_bar_tempo_por_status.png` - Visualização da RQ02
- `docs/rq03_bar_descricao_por_status.png` - Visualização da RQ03
- `docs/rq04_bar_interacoes_por_status.png` - Visualização da RQ04
- `docs/rq05_tamanho_vs_revisoes.png` - Visualização da RQ05
- `docs/rq06_tempo_vs_revisoes.png` - Visualização da RQ06
- `docs/rq07_descricao_vs_revisoes.png` - Visualização da RQ07
- `docs/rq08_interacoes_vs_revisoes.png` - Visualização da RQ08

---

*Análise atualizada em 22 de maio de 2026 - Lab03S03*
