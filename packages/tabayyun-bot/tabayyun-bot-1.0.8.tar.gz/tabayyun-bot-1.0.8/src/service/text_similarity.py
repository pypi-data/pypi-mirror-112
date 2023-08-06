from warnings import simplefilter

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)


def get_dataset():
    df = pd.read_csv("/Users/zamzam.badruzaman/Documents/repo/tabayyun-bot/src/dataset/data.csv", delimiter=";")
    return df


def get_vectors(text1, text2):
    vectorizer = CountVectorizer(text1, text2)
    vectorizer.fit([text1, text2])
    return vectorizer.transform([text1, text2]).toarray()


def get_cosine_sim(text: str):
    ds = get_dataset()
    status = "ARTIKEL TIDAK DITEMUKAN"
    link = []
    for _, row in ds.iterrows():
        vectors_content = get_vectors(text.lower(), row['content'].lower())
        similarity_content = cosine_similarity(vectors_content)
        vectors_tittle = get_vectors(text.lower(), row['tittle'].lower())
        similarity_tittle = cosine_similarity(vectors_tittle)
        if similarity_tittle[0][1] > 0.70 or similarity_content[0][1] > 0.70:
            print(f"Similarity: {similarity_tittle[0][1]} {similarity_content[0][1]}")
            return {"status": row['status'], "link": [row['link']]}
        if text.lower() in row['content'].lower():
            status = "Ditemukan beberapa artikel terkait topik tersebut" \
                if len(set(link)) > 1 else "Ditemukan artikel terkait topik tersebut"
            link.append(f"{row['tittle']} - {row['link']}")

    return {"status": status, "link": set(link)}


if __name__ == '__main__':
    str1 = """Terdapat Sanksi Bagi yang Berkendara Malam di Jakarta"""
    get_dataset()
    print(get_cosine_sim(str1))
