import pandas
from pandas import read_csv, DataFrame
import time
from datetime import datetime
from matplotlib import pyplot as plt


""" DATA LOAD & PREPROCESSING """
dataset = read_csv('./dataset.csv')
f_dataset = pandas.DataFrame({'brand_id' : list(dataset['brand_id']), 'date' : list(dataset['date']), 'call_start_time' : list(dataset['call_start_time'])})

dataset_pizza = f_dataset[:][(dataset['brand_id'] == 'MRPIZZA')]
dataset_chicken = f_dataset[:][(dataset['brand_id'] == 'BBQ')]

# int로 되어 있는 시,분,초 -> str + hour 단위       ex) 120159 -> '12'
col_name_list_pizza = list(dataset_pizza)
col_name_list_chicken = list(dataset_chicken)
values_pizza = dataset_pizza.values
values_chicken = dataset_chicken.values

for i in range(len(values_pizza)):
    values_pizza[i,1] = str(values_pizza[i,1])
    if len(values_pizza[i,1]) != 6:
        zero_count = 6 - len(values_pizza[i,1])
        values_pizza[i,1] = '0' * zero_count + values_pizza[i,1]
    values_pizza[i,1] = values_pizza[i,1][0:2]

for i in range(len(values_chicken)):
    values_chicken[i,1] = str(values_chicken[i,1])
    if len(values_chicken[i,1]) != 6:
        zero_count = 6 - len(values_chicken[i,1])
        values_chicken[i,1] = '0' * zero_count + values_chicken[i,1]
    values_chicken[i,1] = values_chicken[i,1][0:2]

dataset_pizza = pandas.DataFrame(values_pizza)
dataset_chicken = pandas.DataFrame(values_chicken)
dataset_pizza.columns = col_name_list_pizza
dataset_chicken.columns = col_name_list_chicken

# 시간대 별 call count
visual_pizza = dataset_pizza.groupby(['call_start_time']).count()
visual_chicken = dataset_chicken.groupby(['call_start_time']).count()

# call count -> call ratio
pizza_ratio = []
chicken_ratio = []

tot_count = sum(visual_pizza['brand_id'])
for i in range(len(visual_pizza)):
    pizza_ratio.append(visual_pizza['brand_id'][i] / tot_count)

tot_count = sum(visual_chicken['brand_id'])
for i in range(len(visual_chicken)):
    chicken_ratio.append(visual_chicken['brand_id'][i] / tot_count)


""" VISUALIZATION """
visual_pizza['ratio'] = pizza_ratio
visual_chicken['ratio'] = chicken_ratio

# chicken은 09시간대 주문 없고, pizza는 00시간대 주문 없음 -> x label 맞추기 위해 제거
visual_pizza = visual_pizza[visual_pizza.index != '09']
visual_pizza = visual_pizza[visual_pizza.index != '23']
visual_pizza = visual_pizza[visual_pizza.index != '00']
visual_chicken = visual_chicken[visual_chicken.index != '09']
visual_chicken = visual_chicken[visual_chicken.index != '23']
visual_chicken = visual_chicken[visual_chicken.index != '00']

# plot
plt.figure(1)
plt.subplot(211)
plt.plot(list(visual_pizza.index), list(visual_pizza['ratio']), 'b--')
plt.subplot(212)
plt.plot(list(visual_chicken.index), list(visual_chicken['ratio']), 'r--')
plt.show()