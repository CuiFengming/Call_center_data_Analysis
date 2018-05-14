import pandas
from pandas import Series, DataFrame, read_csv
from sklearn.linear_model import LinearRegression
import itertools
from itertools import chain, combinations
import sys
sys.stdout.flush()

#Best Subset Selection
def bss(dataset, target_column):
    dataset = dataset
    target_column = target_column
    dataset = dataset.dropna()
    x_val_count = len(list(dataset)) - 1 # 독립변수 갯수
    y_val = target_column # 종속변수 column name

    predictor_list = []
    r_squared_list = []

    print('%s %22s %6s %s' %('Number of predictors', 'Predictors','R^2', 'Adjusted R^2'))
    #for num_predictor in range(1, x_val_count):
    for num_predictor in range(1, 11):
        res = pandas.DataFrame(columns = ['cols', 'rsquared', 'rsquared_adj'])
        for col_combined in itertools.combinations(dataset.drop(y_val, axis = 1), num_predictor):
            slr = LinearRegression()
            slr.fit(dataset[list(col_combined)], dataset[y_val])
            rsquared = slr.score(dataset[list(col_combined)], dataset[y_val])
            rsquared_adj = 1 - (1 - rsquared) * (dataset.shape[0] - 1) / (dataset.shape[0] - num_predictor - 1)
            res = res.append({'cols': list(col_combined), 'rsquared': rsquared, 'rsquared_adj': rsquared_adj}, ignore_index=True)
    
        print('%d %41s %.4f %.4f' %(num_predictor, res.loc[res['rsquared'].idxmax(),'cols'], res.loc[res['rsquared'].idxmax(),'rsquared'], res.loc[res['rsquared'].idxmax(),'rsquared_adj']), flush = True)
        predictor_list.append(res.loc[res['rsquared'].idxmax(),'cols'])
        r_squared_list.append(res.loc[res['rsquared'].idxmax(),'rsquared_adj'])

    print('\n\n','-------------------------------------------------------------------------', flush = True)
    best_pram_index = r_squared_list.index(max(r_squared_list))
    best_predictor = predictor_list[best_pram_index]
    best_rsquared = r_squared_list[best_pram_index]
    print("best predictor :  ", best_predictor, flush = True)
    print('-------------------------------------------------------------------------','\n\n', flush = True)

    return(best_predictor, best_rsquared)