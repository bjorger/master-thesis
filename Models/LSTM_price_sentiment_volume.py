import math
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras import layers
from Models.helper.MongoDB import MongoDB

from Models.DataScaler import DataScaler
from Models.LSTM_Model import LSTM

tweets = pd.read_csv('analzyed.csv', sep=',')
pricedata = pd.read_csv('lrc_snapshot_2_Nov_9_15.csv', sep=',')
scaler = MinMaxScaler(feature_range=(0,1))
price_data_numeric = pd.to_numeric(pricedata['price'])
sentiment_numeric = pd.to_numeric(tweets['Sentiment'])
volume_numeric = pd.to_numeric(tweets['Volume'])

volumeDataScaler = DataScaler(dataset=volume_numeric, scaler=scaler)
volumeDataScaler.createTrainingData()
volumeDataScaler.createTestData()

sentimentDataScaler = DataScaler(dataset=sentiment_numeric, scaler=scaler)
sentimentDataScaler.createTrainingData()
sentimentDataScaler.createTestData()

priceDataScaler = DataScaler(dataset=price_data_numeric, scaler=scaler)
priceDataScaler.createTrainingData()
priceDataScaler.createTestData()


"""
plt.figure(figsize=(15, 8))
plt.title('Stock Prices History')
plt.plot(price_data_numeric)
plt.xlabel('Date')
plt.ylabel('Prices ($)')

plt.figure(figsize=(15, 8))
plt.title('Sentiment')
plt.plot(tweets['Sentiment'])
plt.xlabel('Date')
plt.ylabel('Sentiment')
"""

model = LSTM(inputs=[priceDataScaler, sentimentDataScaler, volumeDataScaler], scaler=scaler)
model.createModel()
model.fit(batch_size=16, epochs=100)

print(model.predictions)
print(model.rmse)

data = price_data_numeric
train = data[:priceDataScaler.train_data_len]

validation = pd.DataFrame()
validation['price'] = data[priceDataScaler.train_data_len:]
validation['Predictions'] = model.predictions

"""
plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Date')
plt.ylabel('Close Price USD ($)')
plt.plot(train)
plt.plot(validation[['price', 'Predictions']])
plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
plt.show()

plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Date')
plt.ylabel('Close Price USD ($)')
plt.plot(validation[['price', 'Predictions']])
plt.legend(['Val', 'Predictions'], loc='lower right')
plt.show()
"""

#RMSE 0.14439778669565098