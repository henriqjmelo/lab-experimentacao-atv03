# Lab03S03: Análise de Dados e Visualizações

## Resumo Executivo

Análise completa de 46.165 Pull Requests de 156 repositórios populares do GitHub, investigando a influência de variáveis no merge de PRs e no número de revisões.

---

## Metodologia de Análise

### 1. Preparação dos Dados

**Dataset:** 46.165 PRs de 156 repositórios populares
- **PRs MERGED:** 34.579 (74,9%)
- **PRs CLOSED:** 11.586 (25,1%)

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

#### A. Mann-Whitney U Test (Questões RQ01-RQ04)

**Quando usar:** Comparação de duas populações independentes com distribuição não-normal

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

**Quando usar:** Medir associação monotônica entre duas variáveis contínuas

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
p-value: 0.2326
Mediana MERGED: 76 linhas
Mediana CLOSED: 78 linhas
```
**Resultado:** Sem diferença significativa (p > 0.05)

#### RQ 02: Tempo de Análise vs Feedback Final

```
Teste Mann-Whitney U para Duração
p-value: 0.5371
Mediana MERGED: 12.29 horas
Mediana CLOSED: 12.19 horas
```
**Resultado:** Sem diferença significativa (p > 0.05)

#### RQ 03: Descrição vs Feedback Final

```
Teste Mann-Whitney U para Descrição
p-value: 0.3221
Mediana MERGED: 209 caracteres
Mediana CLOSED: 205 caracteres
```
**Resultado:** Sem diferença significativa (p > 0.05)

#### RQ 04: Interações vs Feedback Final

```
Teste Mann-Whitney U para Interações
p-value: 0.2011
Mediana MERGED: 32 interações
Mediana CLOSED: 33 interações
```
**Resultado:** Sem diferença significativa (p > 0.05)

---

### B. Número de Revisões

#### RQ 05: Tamanho vs Número de Revisões

```
Correlação Spearman (Linhas Adicionadas):
ρ = 0.6171, p-value < 0.0001
```
**Resultado:** Correlação positiva moderada SIGNIFICATIVA

#### RQ 06: Tempo de Análise vs Número de Revisões

```
Correlação Spearman:
ρ = -0.0081, p-value = 0.0820
```
**Resultado:** Sem correlação significativa (p > 0.05)

#### RQ 07: Descrição vs Número de Revisões

```
Correlação Spearman:
ρ = 0.0031, p-value = 0.5077
```
**Resultado:** Sem correlação significativa (p > 0.05)

#### RQ 08: Interações vs Número de Revisões

```
Correlação Spearman:
ρ = 0.5632, p-value < 0.0001
```
**Resultado:** Correlação positiva moderada SIGNIFICATIVA

---

## Visualizações Geradas

### 1. status_analysis.png
Boxplots mostrando distribuição das métricas para PRs MERGED vs CLOSED:
- RQ 01: Tamanho do PR (escala log)
- RQ 02: Tempo de Análise (escala log)
- RQ 03: Tamanho da Descrição (escala symlog)
- RQ 04: Interações Totais (escala log)

### 2. reviews_analysis.png
Scatter plots mostrando relação entre variáveis e número de revisões:
- RQ 05: Tamanho (linhas) vs Revisões
- RQ 06: Tempo de Análise vs Revisões
- RQ 07: Descrição vs Revisões
- RQ 08: Interações vs Revisões

---

## Conclusões

1. **Tamanho do PR não influencia decisão de merge** - Contrário à hipótese inicial
2. **Tempo de análise não diferencia PRs aceitos de rejeitados**
3. **Descrição detalhada não afeta probabilidade de merge**
4. **PRs maiores recebem mais revisões** - Correlação 0.62 (significativa)
5. **Mais interações → mais revisões** - Correlação 0.56 (significativa)

---

## Arquivos Gerados

- `github_prs_data.csv` - Dataset completo (46.165 registros)
- `repositorios_selecionados.csv` - Lista de 156 repositórios
- `repositorios_selecionados.json` - Lista em JSON
- `status_analysis.png` - Visualização de RQ01-04
- `reviews_analysis.png` - Visualização de RQ05-08

---

*Análise realizada em 15 de maio de 2026 - Lab03S03*
