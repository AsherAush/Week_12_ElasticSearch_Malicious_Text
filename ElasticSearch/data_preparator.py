import pandas as pd


class Datapreparation():
    def __init__(self, csv_path='../tweets_injected 3.csv'):
        self.csv_path = csv_path

    def load_data(self):
        df = pd.read_csv(self.csv_path)
        df['TweetID'] = df['TweetID'].apply(lambda x: str(int(float(x))))
        df['CreateDate'] = pd.to_datetime(df['CreateDate'], errors='coerce', utc=True)
        df = df.dropna(subset=['CreateDate'])

        if 'Antisemitic' not in df.columns:
            df['Antisemitic'] = False
        df['Antisemitic'] = df['Antisemitic'].fillna(False).astype(bool)

        return df


# print(Data_preparation())
