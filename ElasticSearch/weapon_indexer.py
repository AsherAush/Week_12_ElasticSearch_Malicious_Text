import nltk
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk, scan

class WeaponsIndexer:
    def __init__(self, connector, index_name="tweets_index", weapons_file="../weapon_list.txt"):
        self.es = connector.get_client()
        self.index = index_name
        self.weapons_list = self.load_weapons_from_file(weapons_file)

    def load_weapons_from_file(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            weapons = [line.strip().lower() for line in f if line.strip()]
        return weapons

    def analyze_and_update(self, size=7000):
        resp = self.es.search(
            index=self.index,
            body={"query": {"match_all": {}}},
            size=size
        )

        actions = []
        for hit in resp['hits']['hits']:
            tweet_id = hit['_id']
            text = hit['_source'].get('text', "").lower()

            found_weapons = [weapon for weapon in self.weapons_list if weapon in text]

            if found_weapons:
                action = {
                    "_op_type": "update",
                    "_index": self.index,
                    "_id": tweet_id,
                    "doc": {
                        "weapons_found": found_weapons
                    }
                }
                actions.append(action)

        if actions:
            helpers.bulk(self.es, actions)
            print(f"עודכנו {len(actions)} מסמכים עם שדה weapons_found.")
        else:
            print("לא נמצאו כלי נשק במסמכים.")
