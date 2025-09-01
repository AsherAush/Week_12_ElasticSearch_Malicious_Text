import pandas as pd


def Data_preparation():
    df = pd.read_csv('../tweets_injected 3.csv')
    df['TweetID'] = df['TweetID'].apply(lambda x: str(int(float(x))))

    # שמירה כ-datetime בפורמט שה-Elasticsearch אוהב
    df['CreateDate'] = pd.to_datetime(df['CreateDate'], errors='coerce', utc=True)
    df = df.dropna(subset=['CreateDate'])


    # לוודא שדה Antisemitic
    if 'Antisemitic' not in df.columns:
        df['Antisemitic'] = False
    df['Antisemitic'] = df['Antisemitic'].fillna(False).astype(bool)

    return df


print(Data_preparation())
