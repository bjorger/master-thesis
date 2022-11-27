import yfinance as yf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from helper.DataScaler import DataScaler
from helper.LSTM_Model import LSTM

tweets = pd.read_csv('analzyed.csv', sep=',')
pricedata = pd.read_csv('lrc_snapshot_2_Nov_9_15.csv', sep=',')
scaler = MinMaxScaler(feature_range=(0,1))

price_data_numeric = pd.to_numeric(pricedata['price'])
sentiment_data_numeric = pd.to_numeric(tweets['Sentiment'])

batch_train = 68
batch_predict = 45
interval = 12
epoch = 100

sentimentDataScaler = DataScaler(dataset=sentiment_data_numeric, scaler=scaler, interval=interval)
sentimentDataScaler.createTrainingData()
sentimentDataScaler.createTestData()

priceDataScaler = DataScaler(dataset=price_data_numeric, scaler=scaler, interval=interval)
priceDataScaler.createTrainingData()
priceDataScaler.createTestData()

model = LSTM(inputs=[priceDataScaler], scaler=scaler)
model.create_model(batch_train)
model.train_model('price_sentiment', 100, batch_train)
model.create_model(batch_predict)
model.predict('price_sentiment')

print(model.predictions)
print('RMSE: {}, Batch Size Train: {}, Batch Size Predict: {}'.format(model.rmse, batch_train, batch_predict))

data = price_data_numeric
train = data[:priceDataScaler.train_data_len]

validation = pd.DataFrame()
validation['price'] = data[priceDataScaler.train_data_len:]
validation['Predictions'] = model.predictions

plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Date')
plt.ylabel('Close Price USD ($)')
plt.plot(validation[['price', 'Predictions']])
plt.legend(['Val', 'Predictions'], loc='lower right')
plt.show()


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

#RMSE 0.13071630044668092