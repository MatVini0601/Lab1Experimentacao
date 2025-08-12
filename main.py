import requests
import csv
import datetime
import statistics

# === CONFIGURAÇÃO ===
GITHUB_TOKEN = ""
OUTPUT_FILE = "repos_populares.csv"
RESUMO_FILE = "estatisticas_resumo.csv"

# === QUERY GRAPHQL ===
query = """
query($cursor: String) {
  search(query: "stars:>0 sort:stars-desc", type: REPOSITORY, first: 10, after: $cursor) {
    pageInfo {
      endCursor
      hasNextPage
    }
    edges {
      node {
        ... on Repository {
          name
          owner { login }
          createdAt
          updatedAt
          primaryLanguage { name }
          pullRequests(states: MERGED) { totalCount }
          releases { totalCount }
          issues { totalCount }
          closed: issues(states: CLOSED) { totalCount }
          stargazerCount
          url
        }
      }
    }
  }
}
"""

def run_query(variables):
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers
    )
    if response.status_code != 200:
        raise Exception(f"Erro {response.status_code}: {response.text}")
    return response.json()

def calcular_estatisticas(lista):
    if not lista:
        return {"min": None, "max": None, "media": None, "mediana": None}
    return {
        "min": min(lista),
        "max": max(lista),
        "media": round(statistics.mean(lista), 2),
        "mediana": round(statistics.median(lista), 2)
    }

def main():
    repos = []
    cursor = None
    total_fetched = 0

    while total_fetched < 100:
        data = run_query({"cursor": cursor})
        search_data = data["data"]["search"]
        
        for edge in search_data["edges"]:
            repo = edge["node"]

            # Cálculos
            created_at = datetime.datetime.fromisoformat(repo["createdAt"].replace("Z", "+00:00"))
            updated_at = datetime.datetime.fromisoformat(repo["updatedAt"].replace("Z", "+00:00"))
            idade_dias = (datetime.datetime.utcnow() - created_at.replace(tzinfo=None)).days
            dias_ultima_atualizacao = (datetime.datetime.utcnow() - updated_at.replace(tzinfo=None)).days
            total_issues = repo["issues"]["totalCount"]
            closed_issues = repo["closed"]["totalCount"]
            percentual_issues_fechadas = (closed_issues / total_issues * 100) if total_issues > 0 else 0

            repos.append({
                "name": repo["name"],
                "owner": repo["owner"]["login"],
                "url": repo["url"],
                "stars": repo["stargazerCount"],
                "primary_language": repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else None,
                "idade_dias": idade_dias,
                "pull_requests_aceitas": repo["pullRequests"]["totalCount"],
                "total_releases": repo["releases"]["totalCount"],
                "dias_desde_ultima_atualizacao": dias_ultima_atualizacao,
                "percentual_issues_fechadas": round(percentual_issues_fechadas, 2)
            })

        total_fetched += len(search_data["edges"])
        print(f"Coletados: {total_fetched}")
        
        if not search_data["pageInfo"]["hasNextPage"]:
            break
        cursor = search_data["pageInfo"]["endCursor"]

    # Salvar em CSV com todos os dados
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = repos[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(repos)

    print(f"Arquivo salvo: {OUTPUT_FILE}")

    # Gerar estatísticas
    estatisticas = [
        {"RQ": "RQ01 - Idade do repositório (dias)", **calcular_estatisticas([r["idade_dias"] for r in repos])},
        {"RQ": "RQ02 - Pull requests aceitas", **calcular_estatisticas([r["pull_requests_aceitas"] for r in repos])},
        {"RQ": "RQ03 - Total releases", **calcular_estatisticas([r["total_releases"] for r in repos])},
        {"RQ": "RQ04 - Dias desde última atualização", **calcular_estatisticas([r["dias_desde_ultima_atualizacao"] for r in repos])},
        {"RQ": "RQ06 - % Issues fechadas", **calcular_estatisticas([r["percentual_issues_fechadas"] for r in repos])},
    ]

    # Salvar resumo
    with open(RESUMO_FILE, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["RQ", "min", "max", "media", "mediana"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(estatisticas)

    print(f"Arquivo de resumo salvo: {RESUMO_FILE}")

if __name__ == "__main__":
    main()
