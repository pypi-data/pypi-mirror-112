import os
import sys
from sqlite3 import connect
from warnings import simplefilter

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)
project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(project_dir)


def get_dataset(dataset_db: str):
    conn = connect(dataset_db)
    df = pd.read_sql("select link, tittle, content, status from articles", conn)
    return df


def get_vectors(text1, text2):
    vectorizer = CountVectorizer(text1, text2)
    vectorizer.fit([text1, text2])
    return vectorizer.transform([text1, text2]).toarray()


def get_cosine_sim(text: str):
    if os.environ.get('HOAX_DATABASE'):
        dataset_path = os.environ.get('HOAX_DATABASE')
    else:
        dataset_path = os.path.join(project_dir, "dataset/tabayyun.db")
    ds = get_dataset(dataset_path)
    status = "ARTIKEL TIDAK DITEMUKAN"
    link = []
    for _, row in ds.iterrows():
        vectors_content = get_vectors(text.lower(), row['content'].lower())
        similarity_content = cosine_similarity(vectors_content)
        vectors_tittle = get_vectors(text.lower(), row['tittle'].lower())
        similarity_tittle = cosine_similarity(vectors_tittle)
        if similarity_tittle[0][1] > 0.70 or similarity_content[0][1] > 0.70:
            print(f"Similarity: {similarity_tittle[0][1]} {similarity_content[0][1]}")
            return {"content": row['content'], "status": row['status'], "link": [row['link']]}
        if text.lower() in row['content'].lower():
            status = "Ditemukan beberapa artikel terkait topik tersebut" \
                if len(set(link)) > 1 else "Ditemukan artikel terkait topik tersebut"
            link.append(f"{row['tittle']} - {row['link']}")

    return {"content": text, "status": status, "link": set(link)}


if __name__ == '__main__':
    str1 = """Terdapat Sanksi Bagi yang Berkendara Malam di Jakarta"""
    print(get_cosine_sim(str1))
