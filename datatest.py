import json
import os

from elasticsearch import Elasticsearch

# test_json_path = os.path.join("data", "test.json")
# file = open(test_json_path, 'r', encoding='utf-8')
# data = []
#
# for line in file.readlines():
#     dic = json.loads(line)
#     data.append(dic)
#
# crime_small = []
# tezheng = []
# rending = []
# fatiao = []
# chufa = []
# jieshi = []
# bianhu = []
# crime_big = []
# gainian = []
# for i in range(len(data)):
#     crime_big.append(data[i]['crime_big'])
#     gainian.append(data[i]['gainian'])
#     crime_small.append(data[i]['crime_small'])
#     tezheng.append(data[i]['tezheng'])
#     rending.append(data[i]['rending'])
#     fatiao.append(data[i]['fatiao'])
#     chufa.append(data[i]['chufa'])
#     jieshi.append(data[i]['jieshi'])
#     bianhu.append(data[i]['bianhu'])
# , http_auth=("elastic", "1h=jkBFRwUebMoW30lAH")

es = Elasticsearch('http://192.168.78.128:9200', http_auth=("elastic", "1h=jkBFRwUebMoW30lAH"))
print(es)
doc_type = "loyal"
node_mappings = {
    "mappings": {
        doc_type: {  # type
            "properties": {
                "question": {  # field: 问题
                    "type": "text",  # lxw NOTE: cannot be string
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_smart",
                    "index": "true"  # The index option controls whether field values are indexed.
                },
                "answers": {  # field: 问题
                    "type": "text",  # lxw NOTE: cannot be string
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_smart",
                    "index": "true"  # The index option controls whether field values are indexed.
                },
            }
        }
    }
}
res = es.index(index=doc_type, id=1, document=node_mappings)
print(res)