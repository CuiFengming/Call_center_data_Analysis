import numpy as np
from numpy import concatenate
from math import sqrt
import pandas
from pandas import Series, DataFrame, concat, read_csv

from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM, Conv1D, MaxPool1D, Activation, MaxPooling1D

import itertools
from itertools import chain, combinations
from datetime import datetime
import time

import matplotlib.pyplot as plt
import sys
sys.stdout.flush()

from preprocessing import preprocessing
from best_subset_selection import bss


# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	df = DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

def tsa(dataset, best_predictor, target_column):
    if 'Day' not in best_predictor:
        best_predictor.insert(0,'Day')   # bss에서 date 컬럼이 안잡히는 경우, date 컬럼은 가장 앞에 추가.

    best_predictor.append(target_column)  # forecast dataset 만들기 위해 best predictor에 y value 합치기
    f_dataset = dataset[best_predictor]

    #f_dataset에서 문자 -> datetime
    col_name_list = list(f_dataset)
    values = f_dataset.values
    date_list = values[:,0]

    date_list2 = [datetime.strptime(str(x), '%Y%m%d') for x in date_list]
    values[:,0] = date_list2
    f_dataset = pandas.DataFrame(values)
    f_dataset.columns= col_name_list

    # set 'Day' column -> index
    f_dataset = f_dataset.set_index('Day')

    # X dataset, Y dataset Order setting(y가 제일 좌측으로)
    x_val_list = []
    for x_element in best_predictor:
        if x_element != target_column and x_element != 'Day':
            x_val_list.append(x_element) 

    x_val_list.insert(0,target_column)

    f_dataset = f_dataset[x_val_list]
    f_values = f_dataset.values
    f_values = f_values.astype('float32')

    # normalize features
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled = scaler.fit_transform(f_values)

    n_hour = 1
    n_features = len(f_dataset.columns)

    # frame as supervied learning
    reframed = series_to_supervised(scaled,n_hour,1)  # 1,1 : t-1 t-2 어디까지 볼건지 결정

    # split into train and test sets
    values = reframed.values
    n_train_hours = 30 * 14 #14개월 데이터로 5개월 예측
    train = values[:n_train_hours, :]
    test = values[n_train_hours:-40, :]

    # split into input and outputs
    n_obs = n_hour * n_features
    train_X, train_y = train[:, :n_obs], train[:, -n_features]
    test_X, test_y = test[:, :n_obs], test[:, -n_features]

    # reshape input to be 3D [samples, timesteps, features]
    train_X = train_X.reshape((train_X.shape[0], n_hour, n_features))
    test_X = test_X.reshape((test_X.shape[0], n_hour, n_features))
    
    # design network
    model = Sequential()
    model.add(Conv1D(input_shape=(train_X.shape[1], train_X.shape[2]) , filters = 100, kernel_size= 84, activation='relu',padding='same'))
    model.add(MaxPooling1D(pool_size=1))
    model.add(LSTM(100, dropout = 0.2 ,input_shape=(train_X.shape[1], train_X.shape[2])))
    model.add(Dense(1))
    model.compile(loss='mae', optimizer='adam')

    # fit network
    history = model.fit(train_X, train_y, epochs=100, batch_size=72, validation_data=(test_X, test_y), verbose=2, shuffle=True)

    # plot history
    #plt.plot(history.history['loss'], label='train')
    #plt.plot(history.history['val_loss'], label='test')
    #plt.show()
    #model.save('./tsa_model')
    return (model, n_hour, n_features, scaler, test_X, test_y)