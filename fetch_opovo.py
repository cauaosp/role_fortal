import json
import time

import requests
from bs4 import BeautifulSoup
from utils.functions import creation_time


def fetch_opovo(url, params, headers):
    opovo_articles = []

    params["offset"] = 30

    try:
        response = requests.get(url, params=params, headers=headers)
        print(response.status_code, "opovo")
        data = response.json()

        created_at = creation_time()
        for item in data:
            try:
                opovo_articles.append(
                    {
                        "titulo": item["ds_matia_titlo"],
                        "subtitulo": item["ds_matia_chape"] or None,
                        "categoria": item["ds_site"],
                        "autor": item["nm_autor"],
                        "dataPublicacao": item["dt_matia_publi"],
                        "link": "https://www.opovo.com.br" + item["ds_matia_path"],
                        "jornal": "opovo",
                        "createdAt": created_at,
                    }
                )
            except KeyError:
                print("Erro ao processar item:", item)
                continue
    except KeyError:
        print("Erro no fetch dos dados")

    return opovo_articles


def fetch_gcmais(url, params, headers):
    gcmais_articles = []

    try:
        response = requests.get(url, params=params, headers=headers)
        print(response.status_code, "gcmais")
        data = response.json()

        created_at = creation_time()

        for item in data:
            try:
                categorias = (
                    item.get("yoast_head_json", {})
                    .get("schema", {})
                    .get("@graph", [{}])[0]
                    .get("articleSection", [])
                )

                gcmais_articles.append(
                    {
                        "titulo": item["title"]["rendered"],
                        "subtitulo": item.get("acf", {}).get("post_gravata"),
                        "categoria": categorias,
                        "autor": item.get("yoast_head_json", {}).get("author"),
                        "dataPublicacao": item["date"],
                        "link": item["link"],
                        "jornal": "gcmais",
                        "createdAt": created_at,
                    }
                )
            except KeyError:
                print("Erro ao processar item:", item)
                continue
    except KeyError:
        print("Erro no fetch dos dados")

    return gcmais_articles


def fetch_dn(url, headers):
    dn_articles = []

    for i in range(3):
        try:
            url_paged = url + f"?page={i + 1}"
            response = requests.get(url_paged, headers=headers)
            print(response.status_code, "diario do nordeste")
            soup = BeautifulSoup(response.text, "html.parser")

            jsonld_script = soup.find("script", {"type": "application/ld+json"})

            if not jsonld_script or jsonld_script.string is None:
                return dn_articles

            data = json.loads(jsonld_script.string)

            if "@graph" in data and len(data["@graph"]) > 0:
                collection_page = data["@graph"][0]

                if "hasPart" in collection_page:
                    for item in collection_page["hasPart"]:
                        if item.get("@type") == "NewsArticle":
                            article = {
                                "title": item.get("headline", ""),
                                "url": item.get("url", ""),
                                "date": item.get("datePublished", ""),
                                "author": item.get("author", {}).get("name", "")
                                if isinstance(item.get("author"), dict)
                                else "",
                                "source": "diariodonordeste",
                            }
                            dn_articles.append(article)

        except KeyError:
            print("Erro no fetch dos dados")

    return dn_articles


def fetch_oestadoce(url, params, headers):
    oestadoce_articles = []

    try:
        response = requests.get(url, params=params, headers=headers)
        print(response.status_code, "o estado")

        data = response.json()

        created_at = creation_time()

        for item in data:
            try:
                categorias = (
                    item.get("yoast_head_json", {})
                    .get("schema", {})
                    .get("@graph", [{}])[0]
                    .get("articleSection", [])
                )

                oestadoce_articles.append(
                    {
                        "titulo": item["title"]["rendered"],
                        "subtitulo": item.get("acf", {}).get("post_gravata"),
                        "categoria": categorias,
                        "autor": item.get("yoast_head_json", {}).get("author"),
                        "dataPublicacao": item["date"],
                        "link": item["link"],
                        "jornal": "oestadoce",
                        "createdAt": created_at,
                    }
                )
            except KeyError:
                print("Erro ao processar item:", item)
                continue

    except KeyError:
        print("Erro no fetch dos dados")

    return oestadoce_articles


def fetch_verdemares(url, headers):
    articles = []

    try:
        response = requests.get(url, headers)
        print(response.status_code, "globoce")

        xml = response.text

        soup = BeautifulSoup(xml, "xml")

        items = soup.find_all("item")[:30]

        for item in items:
            titulo = item.title.text if item.title else None

            subtitulo = (
                item.find("atom:subtitle").text if item.find("atom:subtitle") else None
            )

            link = item.link.text if item.link else None

            data = item.pubDate.text if item.pubDate else None

            categoria = item.category.text if item.category else None

            articles.append(
                {
                    "titulo": titulo,
                    "subtitulo": subtitulo,
                    "categoria": categoria,
                    "dataPublicacao": data,
                    "link": link,
                    "jornal": "g1ceara",
                    "createdAt": creation_time(),
                }
            )

    except KeyError:
        print("Erro no fetch dos dados")

    return articles


if __name__ == "__main__":
    jornais = {
        "opovo": {
            "url": "https://www.opovo.com.br/index.php",
            "params": {
                "id": "/reboot/src/endpoints/VerMais.php",
                "dinamico": 1,
                "site_arvor": "Vida&Arte",
                "offset": 0,
                "limit": 30,
            },
            "headers": {"User-Agent": "Mozilla/5.0"},
        },
        "gcmais": {
            "url": "https://gcmais.com.br/wp-json/wp/v2/posts",
            "params": {
                "categories": "1",
                "page": "1",
                "per_page": "30",
            },
            "headers": {"User-Agent": "Mozilla/5.0"},
        },
        "dn": {
            "url": "https://diariodonordeste.verdesmares.com.br/ceara",
            "headers": {"User-Agent": "Mozilla/5.0"},
        },
        "oestadoce": {
            "url": "https://oestadoce.com.br/wp-json/wp/v2/posts",
            "params": {"categories": "8", "page": "1", "per_page": "30"},
            "headers": {"User-Agent": "Mozilla/5.0"},
        },
        "globoce": {
            "url": "https://g1.globo.com/rss/g1/ce/ceara",
            "headers": {"User-Agent": "Mozilla/5.0"},
        },
    }

    n = 0

    while n == 0:
        data = {"opovo": [], "gcmais": [], "dn": [], "oestadoce": [], "globoce": []}

        data["opovo"].extend(
            fetch_opovo(
                jornais["opovo"]["url"],
                jornais["opovo"]["params"],
                jornais["opovo"]["headers"],
            )
        )
        data["gcmais"].extend(
            fetch_gcmais(
                jornais["gcmais"]["url"],
                jornais["gcmais"]["params"],
                jornais["gcmais"]["headers"],
            )
        )
        data["oestadoce"].extend(
            fetch_oestadoce(
                jornais["oestadoce"]["url"],
                jornais["oestadoce"]["params"],
                jornais["oestadoce"]["headers"],
            )
        )
        data["globoce"].extend(
            fetch_verdemares(jornais["globoce"]["url"], jornais["globoce"]["headers"])
        )

        data["dn"].extend(fetch_dn(jornais["dn"]["url"], jornais["dn"]["headers"]))

        with open("data/artigos_ceara.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"total: {sum(len(v) for v in data.values())} artigos")

        counts = {k: len(v) for k, v in data.items()}
        print(counts)
        n += 1

        # time.sleep(360)
