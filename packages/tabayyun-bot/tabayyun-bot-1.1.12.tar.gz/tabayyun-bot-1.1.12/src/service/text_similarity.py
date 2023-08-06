import os
import sys
from functools import lru_cache
from warnings import simplefilter

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)
project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(project_dir)


@lru_cache()
def get_dataset():
    df = pd.read_pickle("tabayyun.pkl")
    print("get_dataset.cache_info : ", get_dataset.cache_info())
    return df


@lru_cache()
def get_vectors(text1, text2):
    vectorizer = CountVectorizer(text1, text2)
    vectorizer.fit([text1, text2])
    return vectorizer.transform([text1, text2]).toarray()


@lru_cache()
def get_cosine_sim(text: str):
    ds = get_dataset()
    fact = "ARTIKEL TIDAK DITEMUKAN"
    link = []
    for _, row in ds.iterrows():
        vectors_content = get_vectors(text.lower(), row['content'].lower())
        if len(text.split()) > 2:
            similarity_content = cosine_similarity(vectors_content)
            vectors_tittle = get_vectors(text.lower(), row['title'].lower())
            similarity_tittle = cosine_similarity(vectors_tittle)
            if similarity_tittle[0][1] > 0.70 or similarity_content[0][1] > 0.70:
                return {"fact": row['fact'], "classification": row['classification'],
                        "conclusion": row['conclusion'], "references": [row['reference_link']]}

        if text.lower() in row['content'].lower():
            fact = "Ditemukan beberapa artikel terkait topik tersebut" \
                if len(set(link)) > 1 else "Ditemukan artikel terkait topik tersebut"
            link.append(f"{row['title']} - {row['reference_link']}")

    print("get_cosine_sim.cache_info :", get_cosine_sim.cache_info())
    return {"fact": fact, "references": link}


if __name__ == '__main__':
    str1 = """[SALAH] Racikan Air Kelapa Muda, Jeruk Nipis, Garam, dan Madu dapat Membunuh Virus Covid-19"""
    print(get_cosine_sim(str1))
