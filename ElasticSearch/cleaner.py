class Cleaner:
    def __init__(self, connector, index_name="tweets_index"):
        self.es = connector.get_client()
        self.index = index_name

    def delete_irrelevant(self):
        # מסמכים למחיקה: לא אנטישמיים, אין כלי נשק, רגש ניטרלי או חיובי
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"terms": {"sentiment": ["neutral", "positive"]}}
                    ],
                    "must_not": [
                        {"term": {"antisemitic": True}},
                        {"exists": {"field": "weapons"}}
                    ]
                }
            }
        }

        resp = self.es.delete_by_query(
            index=self.index,
            body=query,
            conflicts="proceed"  # מתעלם מקונפליקטים
        )

        print(f"נמחקו {resp['deleted']} מסמכים לא רלוונטיים.")
