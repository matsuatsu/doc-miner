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


@api.route("/api/network")
class NetworkResource:
    def on_get(self, req, resp):
        resp.text = "test"

    async def on_post(self, req, resp):
        data = await req.media()
        text = data["text"]
        doc = nlp(text)
        results = {}
        nodes = {}
        links = {}
        for sent in doc.sents:
            tokens = [(i, x) for i, x in enumerate(sent)
                      if x.pos_ in ["NOUN", "PROPN"]]
            for i, token in tokens:
                if token.lemma_ not in nodes.keys():
                    c = "black"
                    if token.pos_ == "PROPN":
                        c = "red"
                    nodes[token.lemma_] = {
                        "id": f"{token.lemma_}_{token.pos_}",
                        "name": token.lemma_,
                        "_size": 30,
                        "_color": c
                    }
                elif nodes[token.lemma_]["_size"] < 50:
                    nodes[token.lemma_]["_size"] += 5
            for i in range(len(tokens)):
                for j in range(i+1, len(tokens)):
                    _, token_i = tokens[i]
                    _, token_j = tokens[j]
                    sid = f"{token_i.lemma_}_{token_i.pos_}"
                    tid = f"{token_j.lemma_}_{token_j.pos_}"
                    key = "-".join(sorted([sid, tid]))
                    if key not in links.keys():
                        links[key] = {
                            "sid": sid,
                            "tid": tid,
                            # "_color": "gray",
                            "count": 1
                        }
                    else:
                        links[key]["count"] += 1
        results["nodes"] = list(nodes.values())
        results["links"] = list([x for x in links.values() if x['count'] > 1])
        resp.media = results


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
