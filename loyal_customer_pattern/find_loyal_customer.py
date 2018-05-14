import pandas
from pandas.io import gbq
from matplotlib import pyplot as plt
import operator

######################################################
# Data load & Count call sum
######################################################
query_2016 = """
SELECT sender_number, brand_id, count(DISTINCT(date))
FROM [datamingo:dashboard.tb_pay_call_log]
WHERE date like '2016%'
GROUP BY sender_number, brand_id
HAVING count(call_start_date) < 1000 and sender_number like '010________'
ORDER BY sender_number
LIMIT 500000
"""
data_2016 = pandas.read_gbq(query = query_2016, project_id = 'datamingo')

query_2017 = """
SELECT sender_number, brand_id, count(DISTINCT(date))
FROM [datamingo:dashboard.tb_pay_call_log]
WHERE date like '2017%'
GROUP BY sender_number, brand_id
HAVING count(call_start_date) < 1000 and sender_number like '010________'
ORDER BY sender_number
LIMIT 500000
"""
data_2017 = pandas.read_gbq(query = query_2017, project_id = 'datamingo')

# Call count difference between 2016,2017
data_2016.columns = ['sender_number', 'brand_id', 'count_2016']
data_2017.columns = ['sender_number', 'brand_id', 'count_2017']
print('*-----------------------Count 비교-----------------------*')
print('2016년 단골고객 call count : ', sum(data_2016['count_2016']))
print('2017년 단골고객 call count : ', sum(data_2017['count_2017']))
print('*-------------------------------------------------------*')


######################################################
# Find Loyal Customer pattern
######################################################
# Outer Join & add difference between 2016,2017 column
join_df = pandas.merge(data_2016, data_2017, how = 'outer')
join_df = join_df.fillna(0)
difference_col = []
for i in range(len(join_df)):
    difference_col.append(join_df['count_2017'][i] - join_df['count_2016'][i])
join_df['difference'] = difference_col
print(join_df)

# 2016년보다 2017년에 줄어든 CASE
case1 = join_df[(join_df['difference'] < -5) & (join_df['count_2016'] > 5) & (join_df['count_2017'] < 5 )]
print('\n')
print('*----------------2017년도에 이탈한 단골고객 Case--------------------------*')
print(case1.sort_values(by = ['difference'], ascending = True))
print('총 이탈 Case Count : ',len(case1.index))

decrease_count = {}
for brand in case1['brand_id']:
    if brand in decrease_count:
        decrease_count[brand] += 1
    else:
        decrease_count[brand] = 1

sort_decrease_count = sorted(decrease_count.items(), key = operator.itemgetter(1), reverse = True)
print('\n')
print('*----------------2017년도에 이탈한 단골고객 많은 브랜드--------------------------*')
print(sort_decrease_count)


# 2016년보다 2017년에 증가한 CASE
join_df['difference'] = difference_col
case2 = join_df[(join_df['difference'] > 5) & (join_df['count_2016'] != 0) & (join_df['count_2017'] > 5 )]
print('\n')
print('*----------------2017년도에 유입된 단골고객 Case--------------------------*')
print(case2.sort_values(by = ['difference'], ascending = False))
print('총 유입 Case Count : ',len(case2.index))

increase_count = {}
for brand in case2['brand_id']:
    if brand in increase_count:
        increase_count[brand] += 1
    else:
        increase_count[brand] = 1

sort_increase_count = sorted(increase_count.items(), key = operator.itemgetter(1), reverse = True)
print('\n')
print('*----------------2017년도에 유입한 단골고객 많은 브랜드--------------------------*')
print(sort_increase_count)


######################################################
# Visualization
######################################################
visual_2016 = list(join_df['count_2016'])
visual_2017 = list(join_df['count_2017'])

# visualization_1
plt.figure(1)
plt.subplot(211)
plt.ylim(ymax=200)
plt.plot(visual_2016)
plt.subplot(212)
plt.ylim(ymax=200)
plt.plot(visual_2017)
plt.show()

# visualization_2
plt.plot(visual_2016, 'r--', visual_2017, 'b--')
plt.show()