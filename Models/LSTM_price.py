import yfinance as yf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from helper.DataScaler import DataScaler
from helper.LSTM_Model import LSTM


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


pricedata = pd.read_csv('helper/data/lrc_snapshot.csv', sep=',')
scaler = MinMaxScaler(feature_range=(0,1))
price_data_numeric = pd.to_numeric(pricedata['price'])

batch_train = 68
batch_predict = 45
interval = 12
epoch = 100

priceDataScaler = DataScaler(dataset=price_data_numeric, scaler=scaler, interval=interval)
priceDataScaler.createTrainingData()
priceDataScaler.createTestData()

model = LSTM(inputs=[priceDataScaler], scaler=scaler)
#https://stackoverflow.com/questions/43702481/why-does-keras-lstm-batch-size-used-for-prediction-have-to-be-the-same-as-fittin
model.create_model(batch_train)
model.train_model('price', 100, batch_train)
model.create_model(batch_predict)
model.predict('price')

print(model.predictions)
print('RMSE: {}, Batch Size Train: {}, Batch Size Predict: {}'.format(model.rmse, batch_train, batch_predict))

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
"""

plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Date')
plt.ylabel('Close Price USD ($)')
plt.plot(validation[['price', 'Predictions']])
plt.legend(['Val', 'Predictions'], loc='lower right')
plt.show()


# RMSE 0.1408308510371961 (Interval 6) / 0.1361816589423932 (layered LSTM)
# RMSE 0.13780698819845097 (Interval 12) / 0.1311678205320157 (layered LSTM)
# RMSE 0.1365049843379773 (Interval 24) / 0.13724269612520115 (layered LSTM)

# RMSE 0.1090287877411312 (Interval 12) / Layered 