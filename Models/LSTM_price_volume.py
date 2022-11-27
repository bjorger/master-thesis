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
volume_numeric = pd.to_numeric(tweets['Volume'])

volumeDataScaler = DataScaler(dataset=volume_numeric, scaler=scaler)
volumeDataScaler.createTrainingData()
volumeDataScaler.createTestData()

priceDataScaler = DataScaler(dataset=price_data_numeric, scaler=scaler)
priceDataScaler.createTrainingData()
priceDataScaler.createTestData()

model = LSTM(inputs=[priceDataScaler, volumeDataScaler], scaler=scaler)
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

#RMSE 0.13850096507757084