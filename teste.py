import json

import requests
from bs4 import BeautifulSoup
from utils.functions import creation_time


def fetch_cearaagora(url, params, headers):
    articles = []
    print(url, params, headers)

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
        )

        print(response.status_code, "cearaagora")

        items = response.json()

        for item in items:
            author_id = item["author"]
            categorias_id = item.get("categories", [])
            categorias = []

            url_autor = f"https://cearaagora.com.br/wp-json/wp/v2/users/{author_id}"
            autor = requests.get(url_autor, headers=headers).json()

            for i in range(len(categorias_id)):
                url_categoria = f"https://cearaagora.com.br/wp-json/wp/v2/categories/{categorias_id[i]}"
                categoria = requests.get(url_categoria, headers=headers).json()
                categorias.append(categoria["name"])

            articles.append(
                {
                    "titulo": item["title"]["rendered"],
                    "subtitulo": item["excerpt"]["rendered"],
                    "categoria": "",
                    "autor": autor["name"],
                    "dataPublicacao": item["date"],
                    "link": item["link"],
                    "jornal": "cearaagora",
                    "created_at": creation_time(),
                }
            )

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")

    return articles


if __name__ == "__main__":
    jornal = {
        "cearaagora": {
            "url": "https://cearaagora.com.br/wp-json/wp/v2/posts",
            "params": {"page": "1", "per_page": "30"},
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
        }
    }

    articles_list = fetch_cearaagora(
        jornal["cearaagora"]["url"],
        jornal["cearaagora"]["params"],
        jornal["cearaagora"]["headers"],
    )

    print(f"total: {len(articles_list)} artigos")
