import json
from datetime import datetime

import requests


def fetch_opovo(url, params, headers):
    all_data = []

    for i in range(3):  # 3 vezes carregar mais
        params["offset"] = i * 30

        response = requests.get(url, params=params, headers=headers)

        print(url, params, headers)
        print(response.status_code)

        try:
            data = response.json()

            for item in data:
                try:
                    all_data.append(
                        {
                            "titulo": item["ds_matia_titlo"],
                            "subtitulo": item["ds_matia_chape"] or None,
                            "categoria": item["ds_site"],
                            "autor": item["nm_autor"],
                            "dataPublicacao": item["dt_matia_publi"],
                            "link": "https://www.opovo.com.br" + item["ds_matia_path"],
                            "jornal": "opovo",
                            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    )
                except KeyError:
                    print("Erro ao processar item:", item)
                    continue
        except KeyError:
            print("Erro no fetch dos dados")
            continue

    return all_data


if __name__ == "__main__":
    url = "https://www.opovo.com.br/index.php"

    params = {
        "id": "/reboot/src/endpoints/VerMais.php",
        "dinamico": 1,
        "site_arvor": "Vida&Arte",
        "offset": 0,
        "limit": 30,
    }

    headers = {"User-Agent": "Mozilla/5.0"}

    data = fetch_opovo(url, params, headers)

    with open("data/artigos_opovo.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
