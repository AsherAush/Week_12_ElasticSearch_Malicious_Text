from data_preparator import Datapreparation
from elasticsearch_connector import ElasticsearchConnector
from elasticsearch_manager import ElasticsearchManager
from sentiment_indexer import SentimentIndexer
from weapon_indexer import WeaponsIndexer
from cleaner import Cleaner


# הכנת דאטה
preparator = Datapreparation()
df = preparator.load_data()

# חיבור ל-ES
connector = ElasticsearchConnector()

# יצירת אינדקס והכנסת דאטה
manager = ElasticsearchManager(connector)
manager.create_index()
manager.bulk_insert(df)
connector.get_client().indices.refresh(index="tweets_index")

# ניתוח סנטימנט והוספתו לאינדקס
sentiment = SentimentIndexer(connector)
sentiment.analyze_and_update()


# זיהוי כלי נשק
weapons = WeaponsIndexer(connector)
weapons.analyze_and_update()


# ניקוי מסמכים לא רלוונטיים
cleaner = Cleaner(connector)
cleaner.delete_irrelevant()
