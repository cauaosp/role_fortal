import json

import requests
from bs4 import BeautifulSoup

url = "https://www.opovo.com.br/vidaearte/"
site = requests.get(url)
soup = BeautifulSoup(site.text, "lxml")

articles = soup.find_all("div", class_="box-listing")

dados = []

for a in articles:
    topper = a.find("span", class_="topper")

    if topper and "portal edicase" in topper.text.lower():
        continue

    categoria = topper.text.strip() if topper else None

    titulo_tag = a.find("h3")
    titulo = titulo_tag.text.strip() if titulo_tag else None

    info = a.find("div", class_="time-category-listing")

    data = None
    autor = None

    if info:
        span = a.find_all("span")

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
        {"titulo": titulo, "categoria": categoria, "autor": autor, "data": data}
    )

print(dados)

# convertendo para json
dados_json = json.dumps(dados, ensure_ascii=False, indent=4)
print(dados_json)

with open("noticias.json", "w", encoding="utf-8") as f:
    f.write(dados_json)
