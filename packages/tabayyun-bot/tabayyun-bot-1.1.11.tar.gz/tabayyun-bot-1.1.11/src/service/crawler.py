import concurrent.futures
import logging
import re
from sqlite3 import IntegrityError

import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

result = []


def crawl(page: str):
    html = requests.get(page)
    bs = BeautifulSoup(html.content, "lxml")

    cards = bs.select("li.card")
    print(f"Crawling {page}, Total News: {len(cards)}")

    for card in cards:
        try:
            url = card.select_one(".title a").get('href')
            title = card.select_one(".title a").text
            title = re.sub(r'(^\[\S+\] )|(^\S+\s?\S+: )', "", title)
            body = card.select_one(".description~.content").text.replace("\n", "")
            status = card.select_one(".status").text.replace("\n", "")
            content = " ".join(body.splitlines())
            result.append([url, title, content, status])

        except Exception as exp:
            logging.warning("Parsing error : %s", exp)


def start(db_path: str = "src/dataset/tabayyun.db", page: int = 3):
    pages = [f"http://cekfakta.com/page/{page_number}" for page_number in range(1, page)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        print("Start concurrent process")
        executor.map(crawl, pages)

    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    df = pd.DataFrame(result, columns=["link", "tittle", "content", "status"])

    for i, _ in enumerate(df.iterrows()):
        try:
            df.iloc[[i]].to_sql('articles', con=engine, if_exists='append', index=False, chunksize=100)
        except IntegrityError as err:
            logging.warning("%s already exist, skip the row!", df.iloc[i]['link'])
            continue


if __name__ == '__main__':
    start("tabayyun.db")
