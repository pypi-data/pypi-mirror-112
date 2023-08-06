import pymongo
import pandas as pd
from datetime import datetime

# 连接数据库
def connect_mongodb(host='127.0.0.1', port=27017):
    mongo_uri = f'mongodb://{host}:{port}/'
    visitor = pymongo.MongoClient(mongo_uri)
    return visitor

# 从mongodb中读取数据库
def query_data(client, database, factors, stocks=None, start_time=None, end_time=None):
    if stocks is None:  # all stocks
        col_dict = {}
    else:
        col_dict = {stock: 1 for stock in stocks}
        col_dict['cal_date'] = 1
    col_dict['_id'] = 0
    if start_time is None and end_time is None:  # all time
        row_dict = {}
    elif start_time is not None and end_time is None:
        start_time = datetime.strptime(start_time, '%Y%m%d')
        row_dict = {'cal_date':{'$gte': start_time}}
    elif start_time is None and end_time is not None:
        end_time = datetime.strptime(end_time, '%Y%m%d')
        row_dict = {'cal_date':{'$lte': end_time}}
    elif start_time is not None and end_time is not None:
        start_time = datetime.strptime(start_time, '%Y%m%d')
        end_time = datetime.strptime(end_time, '%Y%m%d')
        row_dict = {'cal_date':{'$gte': start_time, '$lte': end_time}}
    db = client[database]
    df_dict = {}
    for factor in factors:
        cursor = db[factor].find(row_dict, col_dict)
        df_dict[factor] = pd.DataFrame(list(cursor))
    return df_dict
