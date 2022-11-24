from tensorflow import keras
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from typing import List
import numpy as np
import pandas as pd
import math
from helper.DataScaler import DataScaler
from keras import layers
import keras

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
                    
    def createModel(self):
        inputs = []
        for scaler in self.inputs:
            inputs.append(layers.Input(shape=(scaler.x_train.shape[1], 1)))
        input = layers.Concatenate()(inputs)
        lstm_layer1 = layers.LSTM(100, return_sequences=True)(input)
        lstm_layer2 = layers.LSTM(100, return_sequences=False)(lstm_layer1)
        dense_layer_1 = layers.Dense(25)(lstm_layer2)
        output = layers.Dense(1)(dense_layer_1)
        self.model = keras.models.Model(inputs=inputs, outputs=output)
        self.model.summary()
        
    def fit(self, batch_size = 1, epochs = 5):
        self.model.compile(optimizer='adam', loss='mean_squared_error')
                
        self.model.fit(self.x_train, self.y_train, batch_size=batch_size, epochs=epochs)
        
        predictions = self.model.predict(self.x_test)
        self.predictions = self.scaler.inverse_transform(predictions)
        
        print(self.predictions)
                
        if (len(self.inputs) >= 1): 
            self.rmse = np.sqrt(np.mean(predictions[0] - self.y_test)**2)
        else:
            self.rmse = np.sqrt(np.mean(predictions - self.y_test)**2)
            
        print(self.rmse)
