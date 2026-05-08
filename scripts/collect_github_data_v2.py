import os
import requests
import pandas as pd
import time
from datetime import datetime

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
      }
    }
  }
}
"""

# Query para buscar PRs de um repositório com métricas
PR_QUERY = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
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
    repo_cursor = None
    repos_collected = 0
    
    print("Buscando repositórios populares...")
    while repos_collected < 50: # Vamos pegar os 50 primeiros para garantir volume
        result = run_query(SEARCH_REPOS_QUERY, {"cursor": repo_cursor})
        repos = result['data']['search']['nodes']
        repo_page_info = result['data']['search']['pageInfo']
        
        for repo in repos:
            name_with_owner = repo['nameWithOwner']
            owner, name = name_with_owner.split('/')
            print(f"Processando repo: {name_with_owner}")
            
            pr_cursor = None
            prs_in_repo = 0
            
            try:
                while prs_in_repo < 100:
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
                    if not pr_page_info['hasNextPage'] or len(all_data) > 1000: break
                    pr_cursor = pr_page_info['endCursor']
                    
            except Exception as e:
                print(f"Erro ao processar {name_with_owner}: {e}")
                
            repos_collected += 1
            if len(all_data) >= 1000: break
            
        if not repo_page_info['hasNextPage'] or len(all_data) >= 1000: break
        repo_cursor = repo_page_info['endCursor']

    df = pd.DataFrame(all_data)
    df.to_csv('github_prs_data.csv', index=False)
    print(f"Total de PRs coletados: {len(df)}")

if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN não configurado!")
    else:
        collect_data()
