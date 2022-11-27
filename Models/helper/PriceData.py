from MongoDB import MongoDB
import pandas as pd

mong = MongoDB('lrc_price_snapshots')
df = pd.DataFrame(list(mong.collection.find()))

df.to_csv('./data/lrc_snapshots.csv')