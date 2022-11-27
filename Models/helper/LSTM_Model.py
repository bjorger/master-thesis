from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
from typing import List
import numpy as np
import pandas as pd
from helper.DataScaler import DataScaler
from keras import callbacks
from keras import layers
import keras

earlystopping = callbacks.EarlyStopping(monitor ="loss", 
                                        mode ="min", patience = 5, 
                                        restore_best_weights = True)

class LSTM():
    model = None
    inputs = []
    x_train = []
    x_test = []
    y_train = None
    y_test = None
    predictions = None
    rmse = None
    scaler: MinMaxScaler
    
    def __init__(self, inputs: List[DataScaler], scaler: MinMaxScaler) -> None:
        self.scaler = scaler
        self.inputs = inputs
        self.y_train = inputs[0].y_train
        self.y_test = inputs[0].y_test
        for input in inputs:
            self.x_train.append(input.x_train)
            self.x_test.append(input.x_test)
            
    def create_model(self, batch_size):
        inputs = []
        for scaler in self.inputs:
            inputs.append(layers.Input(batch_shape=(batch_size, scaler.x_train.shape[1], scaler.x_train.shape[2])))
            
        input = layers.Concatenate()(inputs)
        lstm_layer1 = layers.LSTM(100, return_sequences=True, stateful=True)(input)
        lstm_layer2 = layers.LSTM(100, return_sequences=True, stateful=True)(lstm_layer1)
        dropout_layer1 = layers.Dropout(0.3, noise_shape = None, seed = None)(lstm_layer2)
        lstm_layer3 = layers.LSTM(50, return_sequences=True, stateful=True)(dropout_layer1)
        lstm_layer4 = layers.LSTM(25, return_sequences=True, stateful=True)(lstm_layer3)
        # Why flatten here?
        # https://stackoverflow.com/questions/66952606/what-is-this-flatten-layer-doing-in-my-lstm
        flatten_layer = layers.Flatten()(lstm_layer4)
        dense_layer_1 = layers.Dense(25)(flatten_layer)
        output = layers.Dense(1)(dense_layer_1)
        
        self.model = keras.models.Model(inputs=inputs, outputs=output)
        self.model.summary()
                        
    def train_model(self, feature_names: str, epochs, batch_size):
        # Look up best metrics for LSTM
        self.model.compile(optimizer='adam', loss='mean_squared_error', metrics='mae')
                
        self.model.fit(self.x_train, self.y_train, batch_size=batch_size, epochs=epochs, callbacks =[earlystopping])
        
        self.model.save_weights('lstm_{}.h5'.format(feature_names))
        
    def predict(self, feature_names: str, batch_size = 45):
        self.model.load_weights('lstm_{}.h5'.format(feature_names))
        predictions = self.model.predict(self.x_test, batch_size=batch_size)
        self.predictions = self.scaler.inverse_transform(predictions)
                     
        if (len(self.inputs) >= 1): 
            self.rmse = np.sqrt(np.mean(predictions[0] - self.y_test)**2)
        else:
            self.rmse = np.sqrt(np.mean(predictions - self.y_test)**2)
            
        print(self.rmse)
        
