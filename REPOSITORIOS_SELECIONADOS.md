# Laboratório 03: Repositórios Selecionados

## Resumo
- Total de repositórios no recorte final: 200
- Repositórios com dados de PR válidos no dataset: 199
- Critério de seleção de repositório: repositórios populares com >=100 PRs totais (MERGED + CLOSED)
- Data de atualização: 22 de maio de 2026

## Estatísticas da Coleta Final

| Métrica | Valor |
|---------|-------|
| Repositórios no CSV final | 200 |
| Repositórios com PRs no dataset | 199 |
| Total de PRs analisados | 631.440 |
| PRs MERGED | 495.252 (78,43%) |
| PRs CLOSED | 136.188 (21,57%) |

## Critérios Aplicados aos PRs do Dataset

Cada PR incluído no arquivo final atende a:
- Status em MERGED ou CLOSED
- Pelo menos 1 revisão (reviews >= 1)
- Duração >= 1 hora entre criação e fechamento

## Estatísticas Descritivas (Dataset Final)

| Métrica | Mínimo | Mediana | Máximo |
|---------|--------|---------|--------|
| Tamanho total (additions + deletions) | 0 | 40 | 11.143.920 |
| Duração (horas) | 1,0 | 43,12 | 116.725,73 |
| Descrição (caracteres) | 0 | 385 | 229.450 |
| Revisões | 1 | 2 | 1.642 |
| Comentários | 0 | 2 | 694 |
| Participantes | 0 | 3 | 606 |
| Interações totais (participants + comments) | 0 | 5 | 1.300 |

## Observação de Integridade

- O repositório ruanyf/weekly aparece na lista de 200 repositórios, mas não possui PRs no arquivo final de PRs (0 linhas após filtros e/ou retomadas).
- Os demais 199 repositórios possuem dados válidos no dataset.

## Arquivos de Dados

- docs/repositorios_selecionados.csv - Lista final de repositórios (rank, nome, total_prs, prs_analyzed)
- docs/repositorios_selecionados.json - Lista final em JSON
- docs/github_prs_data.csv - Dataset completo de PRs analisados

## Conclusão

A base está consolidada para análise estatística com grande volume de dados e critérios consistentes de filtragem em nível de PR. A lista de repositórios está fechada em 200 entradas e o dataset de PRs contém 631.440 observações válidas.
