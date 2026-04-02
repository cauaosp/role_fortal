import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# buscar usando beautiful soup


def esturuturar_dados(articles):
    dados = []

    for art in articles:
        topper = art.find("span", class_="topper")

        if topper and "portal edicase" in topper.text.lower():
            continue

        categoria = topper.text.strip() if topper else None

        titulo = art.find("h3").text.strip() if art.find("h3") else None

        links = (
            art.find("a", class_="link-listagem").get("href")
            if art.find("a", class_="link-listagem")
            else None
        )

        info = art.find("div", class_="time-category-listing")

        data = None
        autor = None

        if info:
            span = art.find_all("span")

            # data
            for s in span:
                if s.has_attr("timestamp"):
                    data = s["timestamp"]

            # autor
            for s in span:
                if "Por" in s.text:
                    autor = s.text.replace("Por", "").strip()

        # montar o dicionario
        dados.append(
            {
                "titulo": titulo,
                "categoria": categoria,
                "autor": autor,
                "data": data,
                "link": links,
                "jornal": "opovo",
                "CreatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    # convertendo para json
    return json.dumps(dados, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    print("começo do programa")

    url = "https://www.opovo.com.br/vidaearte/"

    hearders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    site = requests.get(url)

    soup = BeautifulSoup(site.text, "lxml")

    articles = soup.find_all("div", class_="box-listing")

    data_json = esturuturar_dados(articles)

    with open("noticias.json", "w", encoding="utf-8") as f:
        f.write(data_json)
