from src.dataclasses.chat import Chat
from src.service.text_similarity import get_cosine_sim


class Server:
    """ The API server """

    @staticmethod
    def handler(chat: Chat):
        similarity = get_cosine_sim(chat.str_message)
        reply: str
        if similarity.get('conclusion'):
            fact = similarity['fact']
            classification = similarity['classification'].upper()
            conclusion = similarity['conclusion']
            references = "\n".join(similarity['references'])
            reply = f"Kategori : {classification} \n\nFakta : \n{fact} \n\nKesimpulan :\n{conclusion} \n\nArtikel terkait:\n{references}"
        elif similarity.get('references'):
            fact = similarity['fact']
            references = "\n".join(similarity['references'])
            reply = f"Konten : \n{chat.str_message} \n\nAnalisa :\n{fact} \n\nArtikel terkait:\n{references}"
        else:
            fact = "Tidak ditemukan artikel terkait konten tersebut"
            content = chat.str_message \
                if len(chat.str_message) < 1000 else f"{chat.str_message[:1000]}....(Sampai akhir)"
            reply = f"Konten : \n{content} \n\nAnalisa : \n{fact}"

        return reply
