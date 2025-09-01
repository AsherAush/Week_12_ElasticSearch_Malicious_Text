from elasticsearch.helpers import bulk


class ElasticsearchManager:
    """connecting to elasticsearch"""
    def __init__(self, connector, index_name='tweets_index', mapping=None):
        self.es = connector.get_client()
        self.index_name = index_name
        self.mapping =  self.default_mapping()


    def default_mapping(self):
        return {
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


    def create_index(self):
        if self.es.indices.exists(index=self.index_name):
            self.es.indices.delete(index=self.index_name)
        self.es.indices.create(index=self.index_name, body=self.mapping)

    def generate_actions(self, df):
        for i, row in df.iterrows():
            yield {
                "_index": self.index_name,
                "_id": f"{row['TweetID']}_{i}",
                "_source": {
                    "TweetID": str(row['TweetID']),
                    "CreateDate": row['CreateDate'],
                    "Antisemitic": bool(row['Antisemitic']),
                    "text": row['text']
                }
            }


    def bulk_insert(self, df):
        """מבצע bulk insert ל־Elasticsearch"""
        bulk(self.es, self.generate_actions(df))





