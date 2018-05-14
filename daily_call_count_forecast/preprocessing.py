import pandas
from pandas import Series, DataFrame, read_csv
from sklearn.preprocessing import LabelEncoder

def preprocessing(target_column):
    # Load dataset(csv) & 지역은 서울에 한정
    dataset = pandas.read_csv('./dataset_final.csv')
    dataset = dataset[:][(dataset['Area_code'] == '002-')]

    # Classify y values to 'Pizza', 'Burger', 'Chicken', 'Total'
    pizza_y = []
    burger_y = []
    chicken_y = []
    total_y = []
    n_x_column = 28

    y_col_list = list(dataset.columns)[n_x_column : ]
    for i in range(len(dataset)):
    	tem_y_value = 0
    	for y in y_col_list:
    		tem_y_value += list(dataset[y])[i]  # y value 브랜드에 상관없이, 통합해서 보기 위함
    	total_y.append(tem_y_value)
    	pizza_y.append(list(dataset['DOMINOPIZZA'])[i] + list(dataset['MRPIZZA'])[i] + list(dataset['PIZZAHUT'])[i] + list(dataset['PIZZAMARU'])[i] + list(dataset['KFC'])[i])
    	burger_y.append(list(dataset['BURGERKING'])[i])
    	chicken_y.append(list(dataset['BHC'])[i] + list(dataset['BBQ'])[i] + list(dataset['GOOBNE'])[i] + list(dataset['NENE'])[i] + list(dataset['CKNIA'])[i])

    dataset= pandas.DataFrame({'Day' : list(dataset['Day']), 'DOW' : list(dataset['DOW']),
    'is_holiday' : list(dataset['is_holiday']), 'Avg_tem' : list(dataset['Avg_tem']), 'High_tem' : list(dataset['High_tem']),
    'Low_tem' : list(dataset['Low_tem']), 'is_fog' : list(dataset['is_fog']), 'is_rain' : list(dataset['is_rain']), 'is_yellow_dust' : list(dataset['is_yellow_dust']),
    'is_snow' : list(dataset['is_snow']),'is_sport_KBO' : list(dataset['is_sport_KBO']),
    'is_sport_NBA' : list(dataset['is_sport_NBA']), 'is_sport_PREMIER' : list(dataset['is_sport_PREMIER']),
    'is_sport_K1' : list(dataset['is_sport_K1']), 'bigmac_local_price' : list(dataset['bigmac_local_price']),
    'bigmac_dollar_price' : list(dataset['bigmac_dollar_price']), 'Product_price_index' : list(dataset['Proudct_price_index']),
    'Consumer_price_index' : list(dataset['Consumer_price_index']), 'KTB_avg_1year' : list(dataset['KTB_avg_1year']),
    'KTB_avg_3year' : list(dataset['KTB_avg_3year']), 'exchange_rate_dollar' : list(dataset['exchange_rate_dollar']),
    'exchange_rate_pound' : list(dataset['exchange_rate_pound']), 'exchange_rate_euro' : list(dataset['exchange_rate_euro']),
    'kospi' : list(dataset['kospi']), 'DOMINOPIZZA' : list(dataset['DOMINOPIZZA']), 'MRPIZZA' : list(dataset['MRPIZZA']), 'BHC' : list(dataset['BHC']),
    'y_pizza' : pizza_y, 'y_burger' : burger_y, 'y_chicken' : chicken_y, 'y_total' : total_y})

    # y값 : pizza에 한정지어서 우선 진행
    dataset = dataset[['Day', 'DOW', 'is_holiday', 'Avg_tem', 'High_tem', 'Low_tem', 'is_fog', 'is_rain', 'is_yellow_dust', 'is_snow','is_sport_KBO', 'is_sport_NBA', 'is_sport_PREMIER', 'is_sport_K1',
     'bigmac_local_price','bigmac_dollar_price','Product_price_index','Consumer_price_index','KTB_avg_1year','KTB_avg_3year',
     'exchange_rate_dollar','exchange_rate_pound','exchange_rate_euro','kospi', target_column]]

    # String(DOW) to float
    col_name_list = list(dataset)
    values = dataset.values

    encoder = LabelEncoder()
    values[:,1] = encoder.fit_transform(values[:,1])
    dataset = pandas.DataFrame(values)
    dataset.columns= col_name_list

    return(dataset)