import logging
import re
from sqlite3 import IntegrityError

import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError


def start(db_path: str = "src/dataset/tabayyun.db", page: int = 3):
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    retry = 0
    max_retry = 2
    result = []
    for page_number in range(1, page):
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
            try:
                url = card.select_one(".title a").get('href')
                title = card.select_one(".title a").text
                title = re.sub(r'(^\[\S+\] )|(^\S+\s?\S+: )', "", title)
                body = card.select_one(".description~.content").text.replace("\n", "")
                status = card.select_one(".status").text.replace("\n", "")
                content = " ".join(body.splitlines())
                result.append([url, title, content, status])

            except Exception:
                continue

    df = pd.DataFrame(result, columns=["link", "tittle", "content", "status"])

    for i, _ in enumerate(df.iterrows()):
        try:
            df.iloc[[i]].to_sql('articles', con=engine, if_exists='append', index=False, chunksize=100)
        except IntegrityError as err:
            logging.warning("%s already exist, skip the row!", df.iloc[i]['link'])
            continue


if __name__ == '__main__':
    start("tabayyun.db")
