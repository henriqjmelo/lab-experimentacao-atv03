import os
import requests
import pandas as pd
import time
from datetime import datetime
import json

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
HEADERS = {'Authorization': f'bearer {GITHUB_TOKEN}'}
URL = 'https://api.github.com/graphql'

def run_query(query, variables):
    response = requests.post(URL, json={'query': query, 'variables': variables}, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed: {response.status_code}. {response.text}")

# Query para buscar repositórios populares
SEARCH_REPOS_QUERY = """
query($cursor: String) {
  search(query: "stars:>10000", type: REPOSITORY, first: 50, after: $cursor) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        nameWithOwner
        pullRequests(states: [MERGED, CLOSED]) {
          totalCount
        }
      }
    }
  }
}
"""

# Query para buscar PRs de um repositório com métricas
PR_QUERY = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    nameWithOwner
    pullRequests(states: [MERGED, CLOSED], first: 50, after: $cursor) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        number
        state
        createdAt
        closedAt
        mergedAt
        bodyText
        additions
        deletions
        changedFiles
        comments {
          totalCount
        }
        reviews(first: 100) {
          totalCount
          nodes {
            author {
              login
            }
          }
        }
        participants(first: 100) {
          totalCount
        }
      }
    }
  }
}
"""

def collect_data():
    all_data = []
    selected_repos = []
    repo_cursor = None
    repos_processed = 0
    repos_selected = 0
    
    print("Buscando repositórios populares (200 maiores)...")
    print("Critério: repositórios com pelo menos 100 PRs (MERGED + CLOSED)")
    print("=" * 70)
    
    while repos_selected < 200:
        result = run_query(SEARCH_REPOS_QUERY, {"cursor": repo_cursor})
        repos = result['data']['search']['nodes']
        repo_page_info = result['data']['search']['pageInfo']
        
        for repo in repos:
            repos_processed += 1
            name_with_owner = repo['nameWithOwner']
            total_prs = repo['pullRequests']['totalCount']
            
            # Validação: repositório deve ter pelo menos 100 PRs
            if total_prs < 100:
                print(f"❌ [{repos_processed}] {name_with_owner} - {total_prs} PRs (rejeitado)")
                continue
            
            repos_selected += 1
            print(f"✅ [{repos_selected}/200] {name_with_owner} - {total_prs} PRs (selecionado)")
            
            owner, name = name_with_owner.split('/')
            
            pr_cursor = None
            prs_in_repo = 0
            prs_with_reviews = 0
            
            try:
                while True:
                    pr_result = run_query(PR_QUERY, {"owner": owner, "name": name, "cursor": pr_cursor})
                    repo_obj = pr_result['data']['repository']
                    if not repo_obj: break
                    
                    prs = repo_obj['pullRequests']['nodes']
                    pr_page_info = repo_obj['pullRequests']['pageInfo']
                    
                    for pr in prs:
                        # Filtros do laboratório
                        if not pr['closedAt']: continue
                        
                        created_at = datetime.strptime(pr['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
                        closed_at = datetime.strptime(pr['closedAt'], '%Y-%m-%dT%H:%M:%SZ')
                        duration_hours = (closed_at - created_at).total_seconds() / 3600
                        
                        # Pelo menos uma hora de duração
                        if duration_hours < 1: continue
                        
                        # Pelo menos uma revisão
                        num_reviews = pr['reviews']['totalCount']
                        if num_reviews < 1: continue
                        
                        prs_with_reviews += 1
                        
                        all_data.append({
                            'repo': name_with_owner,
                            'number': pr['number'],
                            'state': pr['state'],
                            'duration_hours': duration_hours,
                            'additions': pr['additions'],
                            'deletions': pr['deletions'],
                            'changed_files': pr['changedFiles'],
                            'body_len': len(pr['bodyText'] or ""),
                            'participants': pr['participants']['totalCount'],
                            'comments': pr['comments']['totalCount'],
                            'reviews': num_reviews
                        })
                    
                    prs_in_repo += len(prs)
                    if not pr_page_info['hasNextPage']: break
                    pr_cursor = pr_page_info['endCursor']
                    time.sleep(0.5)  # Rate limiting
                    
            except Exception as e:
                print(f"⚠️  Erro ao processar {name_with_owner}: {e}")
            
            print(f"   → {prs_with_reviews} PRs com revisões coletados")
            selected_repos.append({
                'rank': repos_selected,
                'name': name_with_owner,
                'total_prs': total_prs,
                'prs_analyzed': prs_with_reviews
            })
            
            if repos_selected >= 200: break
            
        if not repo_page_info['hasNextPage'] or repos_selected >= 200: break
        repo_cursor = repo_page_info['endCursor']
        time.sleep(1)  # Rate limiting

    # Salvar dataset
    df = pd.DataFrame(all_data)
    df.to_csv('github_prs_data.csv', index=False)
    
    # Salvar lista de repositórios selecionados
    repos_df = pd.DataFrame(selected_repos)
    repos_df.to_csv('repositorios_selecionados.csv', index=False)
    
    # Salvar como JSON também para melhor legibilidade
    with open('repositorios_selecionados.json', 'w', encoding='utf-8') as f:
        json.dump(selected_repos, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 70)
    print(f"✅ COLETA CONCLUÍDA")
    print(f"   • Repositórios selecionados: {repos_selected}")
    print(f"   • Total de PRs coletados: {len(df)}")
    print(f"   • Arquivos salvos:")
    print(f"     - github_prs_data.csv")
    print(f"     - repositorios_selecionados.csv")
    print(f"     - repositorios_selecionados.json")
    print("=" * 70)

if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("❌ ERRO: GITHUB_TOKEN não configurado!")
        print("Execute: export GITHUB_TOKEN='seu_token_aqui'")
    else:
        collect_data()
