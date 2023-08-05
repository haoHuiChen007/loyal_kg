import json
import os
import pymongo

crime_json_path = os.path.join("data", "kg_loyal.json")


def connect_mongo():
    conn = pymongo.MongoClient('mongodb://root:12345@192.168.78.128:27017')


# 由于文件中有多行，直接读取会出现错误，因此一行一行读取
file = open(crime_json_path, 'r', encoding='utf-8')
data = []
for line in file.readlines():
    dic = json.loads(line)
    data.append(dic)

if __name__ == '__main__':
    print(len(data))
