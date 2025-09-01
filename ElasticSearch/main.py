from data_preparator import Datapreparation
from elasticsearch_connector import ElasticsearchConnector
from elasticsearch_manager import ElasticsearchManager
from sentiment_indexer import SentimentIndexer

# הכנת דאטה
preparator = Datapreparation()
df = preparator.load_data()

# חיבור ל-ES
connector = ElasticsearchConnector()

# יצירת אינדקס והכנסת דאטה
manager = ElasticsearchManager(connector)
manager.create_index()
manager.bulk_insert(df)

# ניתוח סנטימנט והוספתו לאינדקס
sentiment = SentimentIndexer(connector)
sentiment.analyze_and_update()
