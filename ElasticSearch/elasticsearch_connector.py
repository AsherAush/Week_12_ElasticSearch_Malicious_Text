from elasticsearch import Elasticsearch

class ElasticsearchConnector:
    def __init__(self, host='http://localhost:9200'):
        self.es = Elasticsearch(host)

    def get_client(self):
        return self.es