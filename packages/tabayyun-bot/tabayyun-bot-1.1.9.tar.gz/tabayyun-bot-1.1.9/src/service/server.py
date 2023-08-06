from src.dataclasses.chat import Chat
from src.service.text_similarity import get_cosine_sim


class Server:
    """ The API server """

    def __init__(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    @staticmethod
    def handler(chat: Chat):
        similarity = get_cosine_sim(chat.str_message)
        if similarity:
            status = similarity['status'].upper()
            link = "\n".join(similarity['link'])
            content = similarity['content']
        else:
            status = "Artikel tidak ditemukan".upper()
            link = "Not Found"
            content = chat.str_message if len(chat.str_message) < 1000 else f"{chat.str_message[:1000]}....(Sampai akhir)"
        reply = f"Konten : \n {content} \n\n Analisa : {status} \n\n Artikel terkait:\n {link}"
        return reply
