import responder
import spacy
from lexrank import LexRank
import pandas as pd

api = responder.API(
    cors=True,
    allowed_hosts=["*"],
    cors_params={"allow_origins": "*",
                 "allow_methods": "*",
                 "allow_headers": "*"
                 })

nlp = spacy.load("en_core_web_sm")


@api.route("/api/ner")
class NerResource:
    def on_get(self, req, resp):
        resp.text = "test"

    async def on_post(self, req, resp):
        data = await req.media()
        text = data["text"]
        doc = nlp(text)
        results = []
        start_id = 0
        end_id = 0
        documents = []
        for sent_id, sent in enumerate(doc.sents):
            tokens = []
            for ent_id, ent in enumerate(sent.ents):
                # 文頭から最初のエンティティまでを追加
                end_id = ent.start_char
                if start_id != end_id:
                    tmp = {
                        'text': text[start_id:end_id],
                        'label': 'O'
                    }
                    tokens.append(tmp)

                start_id = ent.start_char
                end_id = ent.end_char
                tmp = {
                    'id': f"{sent_id}_{ent_id}",
                    'text': text[start_id:end_id],
                    'label': ent.label_
                }
                tokens.append(tmp)
                start_id = ent.end_char
            # 最後のエンティティから文末までを追加
            tokens.append({
                'id': f"{sent_id}_{ent_id+1}",
                'text': text[start_id:sent.end_char],
                'label': 'O'
            })
            start_id = sent.end_char

            tmp = {
                'id': sent_id,
                'sent': tokens
            }
            results.append(tmp)

            extract_tokens = []
            for token in sent:
                if token.pos_ in ['PROPM', 'NOUN', 'VERB', 'ADJ']:
                    extract_tokens.append(token.lemma_)
            documents.append(" ".join(extract_tokens))

        lexrank = LexRank(documents)
        scores = lexrank.rank_sentences(documents, threshold=0.0)
        ranking = pd.Series(scores).rank(
            method="min", ascending=False).tolist()
        for i in range(len(ranking)):
            results[i]['rank'] = int(ranking[i])

        resp.media = results


if __name__ == '__main__':
    api.run(address='0.0.0.0', debug=True)
