import json

import requests
from bs4 import BeautifulSoup
from utils.functions import creation_time


def fetch_cearaagora(url, params, headers):
    print("começo")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(
            "",
            headers=headers,
            timeout=10,  # Evita ficar travado
        )

        if response.status_code == 200:
            post_json = response.json()
            author_id = post_json["author"]
            print(f"Autor: {author_id}")
            categorias = post_json.get("categories", [])
            print(f"Categorias: {categorias}")

            url_autor = f"https://cearaagora.com.br/wp-json/wp/v2/users/{author_id}"
            autor = requests.get(url_autor, headers=headers).json()
            print(f"Nome do autor: {autor['name']}")

            for i in range(len(categorias)):
                url_categoria = f"https://cearaagora.com.br/wp-json/wp/v2/categories/{categorias[i]}"
                categoria = requests.get(url_categoria, headers=headers).json()
                print(f"Categoria {i + 1}: {categoria['name']}")

        else:
            print(f"Erro {response.status_code}: Falha na requisição")

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")


if __name__ == "__main__":
    jornal = {
        "cearaagora": {
            "url": "https://cearaagora.com.br/wp-json/wp/v2/posts/371190",
            "params": {"page": "1", "per_page": "30"},
            "headers": {"User-Agent": "Mozilla/5.0"},
        }
    }

    fetch_cearaagora(
        jornal["cearaagora"]["url"],
        jornal["cearaagora"]["params"],
        jornal["cearaagora"]["headers"],
    )

    # print(f"artigo: {json.dumps(dn_articles_list[0], indent=4)}")
    # print(f"total: {len(dn_articles_list)} artigos")

    # print(json.dumps(dn_articles_list, indent=4))
