from numpy import concatenate
from math import sqrt

from sklearn.metrics import mean_squared_error
from keras.models import load_model

import matplotlib.pyplot as plt
import sys
sys.stdout.flush()

from preprocessing import preprocessing
from best_subset_selection import bss
from build_TSA_model import tsa


""" SETTING """
target_column = 'DOMINOPIZZA' # can be 'DOMINOPIZZA', 'MRPIZZA', 'BHC', 'y_pizza', 'y_burger', 'y_chicken', 'y_total'
dataset = preprocessing(target_column)
dataset = dataset.dropna()
#best_predictor = bss(dataset, target_column)[0]
best_predictor = ['Day', 'DOW', 'is_holiday', 'is_sport_KBO', 'is_sport_NBA', 'is_sport_PREMIER', 'is_sport_K1', 'bigmac_local_price', 'Product_price_index', 'Consumer_price_index', 'KTB_avg_1year', 'KTB_avg_3year', 'exchange_rate_dollar', 'kospi']  #미리 구해둔 최적 x column list
dummy_model, n_hour, n_features, scaler, test_X, test_y = tsa(dataset, best_predictor, target_column)
model = load_model('./tsa_model')


""" MAKE A PREDICTION """
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], n_hour * n_features))

# invert scaling for forecast
testX_col_index = n_features - 1
inv_yhat = concatenate((yhat, test_X[:, -int(testX_col_index):]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]

# invert scaling for actual
test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_y, test_X[:, -int(testX_col_index):]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]

# calculate RMSE
rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)

plt.figure(figsize=(100, 2))
plt.plot(inv_y, label='true value')      #y 실제값
plt.plot(inv_yhat, label='prediction value')   #y 예측값
plt.legend()
plt.ylim((0, max(max(inv_yhat),max(inv_y)) + 200))
plt.show()

# REPORT
#print('예측 기간 간 call count sum -> ', sum(inv_y))
#print('예측 기간 간 call count sum -> ', sum(inv_yhat))
#print('예측 기간 간 예측, 실제 값 차이  -> ', sum(inv_y) - sum(inv_yhat))