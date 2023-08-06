import re

import pandas as pd
import requests
from bs4 import BeautifulSoup


def start(output: str="src/dataset/data.csv"):
    retry = 0
    max_retry = 5
    result = []
    for page_number in range(1, 600):
        print(f"Page: {page_number}")
        html = requests.get(f'http://cekfakta.com/page/{page_number}')
        bs = BeautifulSoup(html.content, "lxml")

        cards = bs.select("li.card")
        print(f"Total News: {len(cards)}")

        if len(cards) == 0:
            if retry == max_retry:
                break

            retry += 1
            continue

        for card in cards:
            url = card.select_one(".title a").get('href')
            status_url = card.select_one(".status a").get('href')
            label = status_url.split("/")[len(status_url.split("/")) - 1]

            if any(data[0] == url for data in result):
                continue
            elif label != "salah" and label != "benar":
                continue

            try:
                title = card.select_one(".title a").text
                title = re.sub(r'(^\[\S+\] )|(^\S+\s?\S+: )', "", title)
                description = card.select_one(".description .content").text.replace("\n", "")
                body = card.select_one(".description~.content").text.replace("\n", "")
                status = card.select_one(".status").text.replace("\n", "")
                content = " ".join(body.splitlines())

                if label == "salah":
                    result.append([url, title, description, "salah", status])

                result.append([url, title, content if label == "salah" else f"{description} {content}", "benar", "Valid"])
            except Exception:
                continue

    df = pd.DataFrame(result, columns=["link", "tittle", "content", "label", "status"])
    df.to_csv(output, sep=";", index=False)


if __name__ == '__main__':
    start("test_data.csv")
