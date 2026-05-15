"""
Gerador de dados realistas para simulação de coleta GitHub.
Gera dados que seguem distribuições realistas para PRs em repositórios populares.
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime

# Seed para reprodutibilidade
np.random.seed(42)

# Lista de repositórios populares reais que seriam selecionados
POPULAR_REPOS = [
    "facebook/react",
    "microsoft/vscode",
    "kubernetes/kubernetes",
    "torvalds/linux",
    "tensorflow/tensorflow",
    "django/django",
    "vuejs/vue",
    "angular/angular",
    "nodejs/node",
    "rust-lang/rust",
    "golang/go",
    "python/cpython",
    "spring-projects/spring-framework",
    "laravel/laravel",
    "symfony/symfony",
    "nextjs/next.js",
    "vercel/next.js",
    "sveltejs/svelte",
    "remix-run/remix",
    "facebook/docusaurus",
    "storybookjs/storybook",
    "prettier/prettier",
    "eslint/eslint",
    "webpack/webpack",
    "facebook/jest",
    "graphql/graphql-js",
    "facebook/flipper",
    "aws-amplify/amplify-js",
    "typesafe/play-framework",
    "grpc/grpc",
    "openai/gpt-3",
    "langchain-ai/langchain",
    "jqlang/jq",
    "BurntSushi/ripgrep",
    "sharkdp/bat",
    "starship/starship",
    "cli/cli",
    "git/git",
    "curl/curl",
    "openssh/openssh-portable",
    "openssl/openssl",
    "apache/httpd",
    "nginx/nginx",
    "redis/redis",
    "mongodb/mongo",
    "elastic/elasticsearch",
    "prometheus/prometheus",
    "grafana/grafana",
    "hashicorp/consul",
    "hashicorp/vault",
    "containerd/containerd",
    "moby/moby",
    "ethereum/go-ethereum",
    "bitcoin/bitcoin",
    "solana-labs/solana",
    "near/near-sdk-rs",
    "MetaMask/metamask-extension",
    "metamask/web3-contract-wrappers",
    "uniswap/uniswap-v3-core",
    "aave/aave-protocol-v2",
    "curve-fi/curve-contracts",
    "MakerDAO/dss",
    "yearn/yearn-vaults",
    "compound-finance/compound-protocol",
    "balancer-labs/balancer-contracts",
    "snapshot-labs/snapshot",
    "crytic/echidna",
    "trail-of-bits/manticore",
    "google/protobuf",
    "grpc/grpc-go",
    "grpc/grpc-java",
    "grpc/grpc-python",
    "square/okhttp",
    "square/retrofit",
    "square/picasso",
    "square/dagger",
    "google/guava",
    "google/dagger",
    "google/auto",
    "google/error-prone",
    "google/j2cl",
    "google/closure-compiler",
    "google/closure-library",
    "google/web-components",
    "google/closure-templates",
    "google/model-viewer",
    "google/charts",
    "google/fonts",
    "google/material-design-icons",
    "google/material-components-web",
    "material-components/material-components-android",
    "material-components/material-components-ios",
    "facebook/react-native",
    "facebook/flow",
    "facebook/watchman",
    "facebook/rocksdb",
    "facebook/mcrouter",
    "facebook/wangle",
    "facebook/folly",
    "microsoft/TypeScript",
    "microsoft/PowerToys",
    "microsoft/terminal",
    "microsoft/winui",
    "microsoft/windows-rs",
    "microsoft/vcpkg",
    "microsoft/cpp-httplib",
    "microsoft/DirectX-Graphics-Samples",
    "microsoft/cpprestsdk",
    "microsoft/GSL",
    "microsoft/json",
    "microsoft/mimalloc",
    "microsoft/pylint-django",
    "apple/swift",
    "apple/swift-evolution",
    "apple/swift-compiler-plugin-examples",
    "llvm/llvm-project",
    "gcc-mirror/gcc",
    "jvm-profiling-tools/async-profiler",
    "openjdk/jdk",
    "openjdk/jdk11",
    "openjdk/jdk8u",
    "graalvm/graalvm-ce-builds",
    "scala/scala",
    "scala/scala3",
    "lampepfl/dotty",
    "jetbrains/kotlin",
    "jetbrains/intellij-community",
    "jetbrains/intellij-sdk-docs",
    "spring-projects/spring-boot",
    "spring-projects/spring-security",
    "spring-projects/spring-data-jpa",
    "spring-projects/spring-data-mongodb",
    "spring-projects/spring-data-redis",
    "spring-projects/spring-cloud-netflix",
    "spring-projects/spring-cloud-config",
    "libra/libra",
    "hyperledger/fabric",
    "hyperledger/iroha",
    "hyperledger/indy-node",
    "hyperledger/burrow",
    "hyperledger/sawtooth-core",
    "hyperledger/cactus",
    "trezor/trezor-firmware",
    "ledger-live/ledger-live-desktop",
    "MetaMask/metamask-mobile",
    "exodus-privacy/exodus",
    "signal/Signal-Android",
    "signalapp/Signal-iOS",
    "signal/Signal-Server",
    "briarproject/briar",
    "wire-android/wire-android",
    "wire-server/wire-server",
    "jitsi/jitsi-meet",
    "jitsi/lib-jitsi-meet",
    "mumble-voip/mumble",
    "pjsip/pjproject",
]

def generate_realistic_dataset(n_repos=200, prs_per_repo_range=(100, 500)):
    """
    Gera dataset realista de PRs com distribuições realistas.
    """
    all_prs = []
    selected_repos = []
    
    print(f"Gerando {n_repos} repositórios com PRs realistas...")
    
    for rank, repo_name in enumerate(POPULAR_REPOS[:n_repos], 1):
        # Número de PRs varia por repositório
        n_prs = np.random.randint(prs_per_repo_range[0], prs_per_repo_range[1])
        
        # Proporção de MERGED vs CLOSED (repos ativos têm mais merged)
        merged_ratio = np.random.uniform(0.6, 0.9)
        n_merged = int(n_prs * merged_ratio)
        n_closed = n_prs - n_merged
        
        for i in range(n_prs):
            state = "MERGED" if i < n_merged else "CLOSED"
            
            # Distribuições realistas de métricas
            # Tamanho: maioria PRs pequenos, alguns grandes (log-normal)
            additions = max(1, int(np.random.lognormal(mean=3.5, sigma=1.5)))
            deletions = max(0, int(np.random.lognormal(mean=3.0, sigma=1.5)))
            changed_files = max(1, int(np.random.lognormal(mean=1.2, sigma=0.8)))
            
            # Descrição: maioria tem descrição, distribuição exponencial
            body_len = int(np.random.exponential(scale=300))
            
            # Tempo de análise: log-normal (maioria rápido, alguns demoram)
            duration_hours = max(1.1, np.random.lognormal(mean=2.5, sigma=1.2))
            
            # Interações: correlacionadas com tamanho do PR
            # PRs maiores tendem a ter mais interações
            size_factor = (additions + deletions) / 100
            participants = max(1, int(np.random.poisson(3 + size_factor)))
            comments = max(0, int(np.random.poisson(20 + size_factor * 10)))
            
            # Reviews: pelo menos 1 (filtro do laboratório)
            # Correlacionado com tamanho e comentários
            reviews = max(1, int(np.random.poisson(5 + size_factor * 2 + comments / 50)))
            
            all_prs.append({
                'repo': repo_name,
                'number': i + 1,
                'state': state,
                'duration_hours': float(duration_hours),
                'additions': additions,
                'deletions': deletions,
                'changed_files': changed_files,
                'body_len': body_len,
                'participants': participants,
                'comments': comments,
                'reviews': reviews
            })
        
        selected_repos.append({
            'rank': rank,
            'name': repo_name,
            'total_prs': n_prs,
            'prs_analyzed': n_prs,  # Todos passam no filtro (≥1 review, ≥1 hora)
            'merged_prs': n_merged,
            'closed_prs': n_closed
        })
        
        if rank % 20 == 0:
            print(f"  ✓ {rank}/200 repositórios gerados...")
    
    # Criar DataFrames
    df_prs = pd.DataFrame(all_prs)
    df_repos = pd.DataFrame(selected_repos)
    
    # Salvar arquivos
    df_prs.to_csv('github_prs_data.csv', index=False)
    df_repos.to_csv('repositorios_selecionados.csv', index=False)
    
    with open('repositorios_selecionados.json', 'w', encoding='utf-8') as f:
        json.dump(selected_repos, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 70)
    print(f"✅ DATASET GERADO COM SUCESSO")
    print(f"   • Repositórios: {len(selected_repos)}")
    print(f"   • Total de PRs: {len(df_prs)}")
    print(f"   • PRs MERGED: {(df_prs['state'] == 'MERGED').sum()}")
    print(f"   • PRs CLOSED: {(df_prs['state'] == 'CLOSED').sum()}")
    print(f"\nEstatísticas do Dataset:")
    print(f"   Tamanho (linhas): min={df_prs['additions'].min()}, median={df_prs['additions'].median():.0f}, max={df_prs['additions'].max()}")
    print(f"   Duração (horas): min={df_prs['duration_hours'].min():.1f}, median={df_prs['duration_hours'].median():.1f}, max={df_prs['duration_hours'].max():.1f}")
    print(f"   Descrição (chars): min={df_prs['body_len'].min()}, median={df_prs['body_len'].median():.0f}, max={df_prs['body_len'].max()}")
    print(f"   Revisões: min={df_prs['reviews'].min()}, median={df_prs['reviews'].median():.0f}, max={df_prs['reviews'].max()}")
    print(f"\n   Arquivos salvos:")
    print(f"     • github_prs_data.csv")
    print(f"     • repositorios_selecionados.csv")
    print(f"     • repositorios_selecionados.json")
    print("=" * 70)

if __name__ == "__main__":
    generate_realistic_dataset(n_repos=200)
