import pymongo
import pandas as pd

# 连接数据库
def connect_mongodb(host='127.0.0.1', port=27017):
    mongo_uri = f'mongodb://{host}:{port}/'
    visitor = pymongo.MongoClient(mongo_uri)
    return visitor

# 从mongodb中读取数据库
def query_data(client, database, factor):
    db = client[database]
    cursor = db[factor].find()
    df = pd.DataFrame(list(cursor))
    del df['_id']
    return df
