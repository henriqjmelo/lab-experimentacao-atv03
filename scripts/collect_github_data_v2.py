import os
import requests
import pandas as pd
import time
from datetime import datetime
import json
import random
import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
HEADERS = {'Authorization': f'bearer {GITHUB_TOKEN}'}
URL = 'https://api.github.com/graphql'
MAX_WORKERS = int(os.getenv('GITHUB_MAX_WORKERS', '2'))
PR_PAGE_SIZE = max(5, min(50, int(os.getenv('GITHUB_PR_PAGE_SIZE', '20'))))
REQUEST_MIN_INTERVAL = float(os.getenv('GITHUB_MIN_INTERVAL', '0.35'))
TRANSIENT_COOLDOWN_SECONDS = int(os.getenv('GITHUB_TRANSIENT_COOLDOWN', '45'))
TARGET_REPOS = max(1, int(os.getenv('GITHUB_TARGET_REPOS', '200')))
FINAL_REPOS = max(1, int(os.getenv('GITHUB_FINAL_REPOS', '200')))
REPO_PAGE_CHECKPOINT_DIR = '.repo_page_checkpoints'

_request_gate_lock = threading.Lock()
_next_request_at = 0.0
_transient_lock = threading.Lock()
_consecutive_transient_errors = 0

def throttle_request_gate():
  global _next_request_at
  with _request_gate_lock:
    now = time.time()
    if now < _next_request_at:
      time.sleep(_next_request_at - now)
    _next_request_at = time.time() + REQUEST_MIN_INTERVAL + random.uniform(0, 0.25)

def mark_success():
  global _consecutive_transient_errors
  with _transient_lock:
    _consecutive_transient_errors = 0

def mark_transient_error_and_maybe_cooldown():
  global _consecutive_transient_errors
  with _transient_lock:
    _consecutive_transient_errors += 1
    current = _consecutive_transient_errors

  if current >= 5:
    cooldown = TRANSIENT_COOLDOWN_SECONDS + random.uniform(0, 5)
    print(f"⏸️  Muitas falhas transitórias em sequência ({current}). Cooldown global de {cooldown:.1f}s...")
    time.sleep(cooldown)
    with _transient_lock:
      _consecutive_transient_errors = 0

def atomic_write_text(file_path, content):
  temp_path = f"{file_path}.tmp"
  with open(temp_path, 'w', encoding='utf-8', newline='') as handle:
    handle.write(content)
  os.replace(temp_path, file_path)

def ensure_repo_checkpoint_dir():
  os.makedirs(REPO_PAGE_CHECKPOINT_DIR, exist_ok=True)

def get_repo_checkpoint_paths(name_with_owner):
  safe_name = name_with_owner.replace('/', '__')
  base_path = os.path.join(REPO_PAGE_CHECKPOINT_DIR, safe_name)
  return {
    'json': f"{base_path}.json",
    'csv': f"{base_path}.csv",
  }

def write_repo_page_checkpoint(name_with_owner, repo_rank, total_prs, prs_analyzed, next_cursor, repo_rows):
  ensure_repo_checkpoint_dir()
  paths = get_repo_checkpoint_paths(name_with_owner)

  pd.DataFrame(repo_rows).to_csv(f"{paths['csv']}.tmp", index=False)
  os.replace(f"{paths['csv']}.tmp", paths['csv'])

  atomic_write_text(
    paths['json'],
    json.dumps({
      'rank': repo_rank,
      'name': name_with_owner,
      'total_prs': total_prs,
      'prs_analyzed': prs_analyzed,
      'next_cursor': next_cursor,
    }, ensure_ascii=False, indent=2),
  )

def load_repo_page_checkpoint(name_with_owner):
  paths = get_repo_checkpoint_paths(name_with_owner)
  if not os.path.exists(paths['json']) or not os.path.exists(paths['csv']):
    return None

  try:
    with open(paths['json'], 'r', encoding='utf-8') as handle:
      metadata = json.load(handle)
    try:
      rows = pd.read_csv(paths['csv']).to_dict('records')
    except pd.errors.EmptyDataError:
      # Keep cursor/metadata even when no valid rows were collected yet.
      rows = []
    return {
      'rank': int(metadata['rank']),
      'name': metadata['name'],
      'total_prs': int(metadata['total_prs']),
      'prs_analyzed': int(metadata['prs_analyzed']),
      'next_cursor': metadata['next_cursor'],
      'rows': rows,
    }
  except Exception as exc:
    print(f"⚠️  Não foi possível carregar checkpoint por página de {name_with_owner}: {exc}")
    return None

def delete_repo_page_checkpoint(name_with_owner):
  paths = get_repo_checkpoint_paths(name_with_owner)
  for path in paths.values():
    if os.path.exists(path):
      os.remove(path)

def write_checkpoint(all_data, selected_repos, repos_selected, is_final=False):
  ordered_repos = sorted(selected_repos, key=lambda repo: repo['rank'])

  df = pd.DataFrame(all_data)
  repos_df = pd.DataFrame(ordered_repos)

  df.to_csv('github_prs_data.csv.tmp', index=False)
  os.replace('github_prs_data.csv.tmp', 'github_prs_data.csv')

  repos_df.to_csv('repositorios_selecionados.csv.tmp', index=False)
  os.replace('repositorios_selecionados.csv.tmp', 'repositorios_selecionados.csv')

  atomic_write_text(
    'repositorios_selecionados.json',
    json.dumps(ordered_repos, ensure_ascii=False, indent=2),
  )

  status = 'final' if is_final else 'parcial'
  print(
    f"💾 Checkpoint {status}: {len(ordered_repos)} repositórios persistidos, "
    f"{len(df)} PRs salvos, alvo atual {repos_selected}/{TARGET_REPOS}"
  )

def load_checkpoint_if_exists():
  all_data = []
  selected_repos = []

  if os.path.exists('github_prs_data.csv'):
    try:
      all_data = pd.read_csv('github_prs_data.csv').to_dict('records')
    except Exception as exc:
      print(f"⚠️  Não foi possível carregar github_prs_data.csv: {exc}")

  if os.path.exists('repositorios_selecionados.csv'):
    try:
      selected_repos = pd.read_csv('repositorios_selecionados.csv').to_dict('records')
      filtered_repos = []
      for repo in selected_repos:
        repo['rank'] = int(repo['rank'])
        repo['total_prs'] = int(repo['total_prs'])
        repo['prs_analyzed'] = int(repo['prs_analyzed'])
        # Ignore placeholder rows created after worker failures.
        if repo['total_prs'] == 0 and repo['prs_analyzed'] == 0:
          print(f"↺ Ignorando placeholder de falha para retomada: {repo['name']}")
          continue
        filtered_repos.append(repo)
      selected_repos = filtered_repos
    except Exception as exc:
      print(f"⚠️  Não foi possível carregar repositorios_selecionados.csv: {exc}")
      selected_repos = []

  return all_data, selected_repos

def run_query(query, variables, max_retries=8, timeout_seconds=45):
  last_error = None
  for attempt in range(1, max_retries + 1):
    try:
      throttle_request_gate()
      response = requests.post(
        URL,
        json={'query': query, 'variables': variables},
        headers=HEADERS,
        timeout=timeout_seconds,
      )

      if response.status_code != 200:
        status = response.status_code
        response_text = response.text or ''

        is_transient = status in {429, 500, 502, 503, 504}
        is_secondary_rate_limit = (
          status == 403 and 'secondary rate limit' in response_text.lower()
        )

        if is_transient or is_secondary_rate_limit:
          mark_transient_error_and_maybe_cooldown()
          if attempt == max_retries:
            raise Exception(f"Query failed: {status}. {response_text}")

          if is_secondary_rate_limit:
            base_wait = min(60, 10 * attempt)
          else:
            base_wait = min(30, 2 ** (attempt - 1))

          jitter = random.uniform(0, 1.5)
          wait_seconds = base_wait + jitter
          print(f"⚠️  Falha transitória da API (HTTP {status}) tentativa {attempt}/{max_retries}")
          print(f"   ↳ aguardando {wait_seconds:.1f}s antes de tentar novamente...")
          time.sleep(wait_seconds)
          continue

        raise Exception(f"Query failed: {status}. {response_text}")

      payload = response.json()
      if 'errors' in payload and payload['errors']:
        raise Exception(f"GraphQL errors: {payload['errors']}")

      mark_success()
      return payload
    except (requests.RequestException, ValueError, Exception) as exc:
      last_error = exc
      if attempt == max_retries:
        break

      mark_transient_error_and_maybe_cooldown()
      backoff = min(30, 2 ** (attempt - 1)) + random.uniform(0, 1.5)
      print(f"⚠️  Falha na chamada da API (tentativa {attempt}/{max_retries}): {exc}")
      print(f"   ↳ aguardando {backoff:.1f}s para nova tentativa...")
      time.sleep(backoff)

  raise Exception(f"Query failed after {max_retries} attempts. Last error: {last_error}")

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
PR_QUERY_TEMPLATE = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    nameWithOwner
    pullRequests(states: [MERGED, CLOSED], first: __PAGE_SIZE__, after: $cursor) {
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
        reviews {
          totalCount
        }
        participants(first: 100) {
          totalCount
        }
      }
    }
  }
}
"""

PR_QUERY = PR_QUERY_TEMPLATE.replace('__PAGE_SIZE__', str(PR_PAGE_SIZE))

def collect_repo_prs(repo_rank, name_with_owner, total_prs):
  owner, name = name_with_owner.split('/')
  pr_cursor = None
  prs_with_reviews = 0
  repo_rows = []

  page_checkpoint = load_repo_page_checkpoint(name_with_owner)
  if page_checkpoint:
    pr_cursor = page_checkpoint['next_cursor']
    prs_with_reviews = page_checkpoint['prs_analyzed']
    repo_rows = page_checkpoint['rows']
    print(
      f"   ↻ retomando {name_with_owner}: {prs_with_reviews} PRs já salvos "
      f"em checkpoint por página"
    )

  while True:
    pr_result = run_query(PR_QUERY, {"owner": owner, "name": name, "cursor": pr_cursor})
    repo_obj = pr_result['data']['repository']
    if not repo_obj:
      break

    prs = repo_obj['pullRequests']['nodes']
    pr_page_info = repo_obj['pullRequests']['pageInfo']

    for pr in prs:
      if not pr['closedAt']:
        continue

      created_at = datetime.strptime(pr['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
      closed_at = datetime.strptime(pr['closedAt'], '%Y-%m-%dT%H:%M:%SZ')
      duration_hours = (closed_at - created_at).total_seconds() / 3600

      if duration_hours < 1:
        continue

      num_reviews = pr['reviews']['totalCount']
      if num_reviews < 1:
        continue

      prs_with_reviews += 1
      repo_rows.append({
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

    next_cursor = pr_page_info['endCursor'] if pr_page_info['hasNextPage'] else None
    write_repo_page_checkpoint(
      name_with_owner,
      repo_rank,
      total_prs,
      prs_with_reviews,
      next_cursor,
      repo_rows,
    )

    if not pr_page_info['hasNextPage']:
      break

    pr_cursor = next_cursor
    time.sleep(0.2)

  return {
    'rank': repo_rank,
    'name': name_with_owner,
    'total_prs': total_prs,
    'prs_analyzed': prs_with_reviews,
    'rows': repo_rows,
  }

def collect_data():
  all_data, selected_repos = load_checkpoint_if_exists()
  existing_repo_names = {repo['name'] for repo in selected_repos}

  repos_selected = len(selected_repos)
  repos_processed = 0
  next_rank = max((repo['rank'] for repo in selected_repos), default=0) + 1

  if repos_selected > 0 or len(all_data) > 0:
    print(
      f"♻️  Retomando de checkpoint: {repos_selected} repositórios e "
      f"{len(all_data)} PRs já carregados"
    )

  repo_cursor = None
  search_done = False
  pending_repos = deque()

  final_target = min(FINAL_REPOS, TARGET_REPOS)

  print(f"Buscando repositórios populares ({TARGET_REPOS} maiores)...")
  print("Critério: repositórios com pelo menos 100 PRs (MERGED + CLOSED)")
  print(f"Workers paralelos: {MAX_WORKERS}")
  print(f"Tamanho de página PR: {PR_PAGE_SIZE}")
  print(f"Intervalo mínimo entre requests: {REQUEST_MIN_INTERVAL}s")
  print(f"Alvo final para entrega: {final_target} repositórios")
  print("=" * 70)

  def fetch_next_repo_page():
    nonlocal repo_cursor, repos_processed, repos_selected, next_rank, search_done

    if search_done or repos_selected >= TARGET_REPOS:
      return

    result = run_query(SEARCH_REPOS_QUERY, {"cursor": repo_cursor})
    repos = result['data']['search']['nodes']
    repo_page_info = result['data']['search']['pageInfo']

    for repo in repos:
      repos_processed += 1
      name_with_owner = repo['nameWithOwner']
      total_prs = repo['pullRequests']['totalCount']

      if name_with_owner in existing_repo_names:
        continue

      if total_prs < 100:
        print(f"❌ [{repos_processed}] {name_with_owner} - {total_prs} PRs (rejeitado)")
        continue

      repo_rank = next_rank
      next_rank += 1
      repos_selected += 1
      existing_repo_names.add(name_with_owner)
      print(f"✅ [{repos_selected}/{TARGET_REPOS}] {name_with_owner} - {total_prs} PRs (selecionado)")
      pending_repos.append((repo_rank, name_with_owner, total_prs))

      if repos_selected >= TARGET_REPOS:
        break

    if not repo_page_info['hasNextPage']:
      search_done = True
    else:
      repo_cursor = repo_page_info['endCursor']
      time.sleep(1)

  with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    in_flight = {}

    while True:
      while len(in_flight) < MAX_WORKERS:
        if not pending_repos:
          if repos_selected >= TARGET_REPOS:
            break
          fetch_next_repo_page()
          if not pending_repos:
            break

        repo_rank, name_with_owner, total_prs = pending_repos.popleft()
        future = executor.submit(collect_repo_prs, repo_rank, name_with_owner, total_prs)
        in_flight[future] = (repo_rank, name_with_owner)

      if not in_flight:
        if repos_selected >= TARGET_REPOS and not pending_repos:
          break
        if search_done and not pending_repos:
          break
        if not pending_repos:
          fetch_next_repo_page()
          if not pending_repos and search_done:
            break
        continue

      done_future = next(as_completed(in_flight))
      repo_rank, name_with_owner = in_flight.pop(done_future)

      try:
        result = done_future.result()
        all_data.extend(result['rows'])
        selected_repos.append({
          'rank': result['rank'],
          'name': result['name'],
          'total_prs': result['total_prs'],
          'prs_analyzed': result['prs_analyzed']
        })
        delete_repo_page_checkpoint(result['name'])
        print(f"   → {result['name']}: {result['prs_analyzed']} PRs com revisões coletados")
        write_checkpoint(all_data, selected_repos, repos_selected)
      except Exception as e:
        if name_with_owner in existing_repo_names:
          existing_repo_names.remove(name_with_owner)
        repos_selected -= 1
        print(f"⚠️  Erro ao processar {name_with_owner}: {e}")
        print(f"   ↻ Repositório será tentado novamente na próxima retomada.")
        write_checkpoint(all_data, selected_repos, repos_selected)

      if search_done and repos_selected >= TARGET_REPOS and not in_flight and not pending_repos:
        break

  # Keep only the first N repositories by rank in final deliverables.
  selected_repos.sort(key=lambda repo: repo['rank'])
  if len(selected_repos) > final_target:
    kept_repos = selected_repos[:final_target]
    kept_names = {repo['name'] for repo in kept_repos}
    all_data = [row for row in all_data if row['repo'] in kept_names]
    selected_repos = kept_repos

  write_checkpoint(all_data, selected_repos, repos_selected, is_final=True)
  df = pd.DataFrame(all_data)

  print("\n" + "=" * 70)
  print("✅ COLETA CONCLUÍDA")
  print(f"   • Repositórios selecionados durante coleta: {repos_selected}")
  print(f"   • Repositórios entregues no CSV final: {len(selected_repos)}")
  print(f"   • Total de PRs coletados: {len(df)}")
  print("   • Arquivos salvos:")
  print("     - github_prs_data.csv")
  print("     - repositorios_selecionados.csv")
  print("     - repositorios_selecionados.json")
  print("=" * 70)

if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("❌ ERRO: GITHUB_TOKEN não configurado!")
        print("Execute: export GITHUB_TOKEN='seu_token_aqui'")
    else:
        collect_data()
