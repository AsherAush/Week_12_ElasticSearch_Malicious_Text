import nltk
from elasticsearch import Elasticsearch, helpers
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')


class SentimentIndexer:
    def __init__(self, index_name="tweets_index", es_host="http://localhost:9200"):
        self.es = Elasticsearch(es_host)
        self.index = index_name
        self.sia = SentimentIntensityAnalyzer()

    def analyze_and_update(self, size=10000):
        resp = self.es.search(
            index=self.index,
            body={"query": {"match_all": {}}},
            size=size
        )

        actions = []
        for hit in resp['hits']['hits']:
            tweet_id = hit['_id']
            text = hit['_source']['text']

            examination = self.sia.polarity_scores(text)
            if examination['compound'] >= 0.05:
                sentiment = 'positive'
            elif examination['compound'] <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'

            action = {
                "_op_type": "update",
                "_index": "tweets_index",
                "_id": tweet_id,
                "doc": {
                    "sentiment": sentiment}
            }
            actions.append(action)

        helpers.bulk(self.es, actions)
        print(f"עודכנו {len(actions)} מסמכים עם שדה sentiment.")


if __name__ == "__main__":
    tagger = SentimentIndexer()
    tagger.analyze_and_update()