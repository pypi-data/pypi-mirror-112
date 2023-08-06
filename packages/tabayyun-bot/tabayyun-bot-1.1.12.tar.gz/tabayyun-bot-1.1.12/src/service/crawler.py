import logging
import os
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


def get_mafindo_data(api_key: str, limit: int) -> list:
    mafindo_data = []
    url = 'https://yudistira.turnbackhoax.id/api/antihoax'
    data = {'key': api_key, 'limit': limit}
    try:
        req = requests.post(url, data=data)
        for response in req.json():
            mafindo_data.append(
                [response['id'],
                 response['authors'],
                 response['status'],
                 response['classification'],
                 response['title'],
                 response['content'],
                 response['fact'],
                 response['references'],
                 response['source_issue'],
                 response['source_link'],
                 response['picture1'],
                 response['picture2'],
                 response['tanggal'],
                 response['tags'],
                 response['conclusion']
                 ])
    except requests.RequestException as exp:
        logging.error(exp)
    return mafindo_data


def start(db_path: str = "src/dataset/tabayyun.db", limit: int = 10):
    api_key = os.environ['MAFINDO_API_KEY']
    mafindo_data = get_mafindo_data(api_key, limit)

    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    mafindo_df = pd.DataFrame(mafindo_data,
                              columns=['id', 'authors', 'status', 'classification', 'title', 'content', 'fact',
                                       'reference_link', 'source_issue', 'source_link', 'picture1', 'picture2', 'tanggal',
                                       'tags', 'conclusion'])

    for i, _ in enumerate(mafindo_df.iterrows()):
        try:
            mafindo_df.iloc[[i]].to_sql('mafindo_tbl', con=engine, if_exists='append', index=False, chunksize=100)
        except IntegrityError:
            logging.warning("%s already exist, skip the row!", mafindo_df.iloc[i]['id'])
            continue


if __name__ == '__main__':
    start("tabayyun.db")
