from  elasticsearch import Elasticsearch
from pprint import pprint
from elasticsearch.helpers import bulk
import data_louder
import pandas as pd


"""connecting to elasticsearch"""
es = Elasticsearch('http://localhost:9200')
print(es.info())
"""creating index"""
index_name = "tweets_index"

if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

mapping = {
    "mappings": {
        "properties": {
            "TweetID": {"type": "keyword"},
            "CreateDate": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
            "Antisemitic": {"type": "boolean"},
            "text":{
                "type": "text",
                "fields":{
                    "raw":{"type": "keyword"}
                }
            }
        }
    }
}
es.indices.create(index=index_name, body=mapping)

df = data_louder.Data_preparation()
def generate_actions(df):
    for i, row in df.iterrows():
        yield {
            "_index": index_name,
            "_id": f"{row['TweetID']}_{i}",
            "_source": {
                "TweetID": str(row['TweetID']),
                "CreateDate": row['CreateDate'],
                "Antisemitic": bool(row['Antisemitic']),
                "text": row['text']
            }
        }




bulk(es, generate_actions(df))


res = es.search(index="tweets_index", query={"match_all": {}}, size=2)
for hit in res["hits"]["hits"]:
    print(hit["_source"])
pprint(res)


