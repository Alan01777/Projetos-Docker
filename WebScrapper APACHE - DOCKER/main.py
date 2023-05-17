from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


def get_TopAnimes(url):
    anime_list = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find("table", class_="top-ranking-table")
    if table is not None:
        for row in table.find_all('tr', class_='ranking-list'):
            rank = row.find('td', class_='rank ac').span.text.strip()
            title = row.find('td', class_='title al va-t word-break').h3.text.strip()
            score = row.find('td', class_='score ac fs14').text.strip()
            infoLines = row.find('td', class_='title al va-t word-break').find(
                "div", class_="information di-ib mt4").text.strip().splitlines()
            ep = infoLines[0].strip()
            date = infoLines[1].strip()
            members = infoLines[2].strip()

            anime_list.append({
                "rank": rank,
                "title": title,
                "score": score,
                "ep": ep,
                "date": date,
                "members": members
            })
        return anime_list
    else:
        print(f"Erro!")
        return None


def createTable(topAnimes):
    df = pd.DataFrame(topAnimes, columns=["rank", "title", "score", "ep", "date", "members"])
    table_html = df.to_html(index=False)
    table_html = table_html.replace('<table border="1" class="dataframe">', '<table>')
    with open("/var/www/localhost/index.html", "w") as f:
        f.write(table_html)
    print("Tabela HTML criada com sucesso em index.html")


def main():
    url = "https://myanimelist.net/topanime.php"
    print("[x] Iniciando busca...")
    try:
        while True:
            topAnimes = get_TopAnimes(url)
            if topAnimes is not None:
                createTable(topAnimes)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[x] Busca interrompida pelo usuário.")
    print("[x] Busca concluída com sucesso.")


if __name__ == "__main__":
    main()