import os
import time
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class ProcessIntoES:
    def __init__(self):
        self._index = "loyal_data"
        self.es = Elasticsearch(hosts=['http://192.168.78.128:9200'],
                                basic_auth=("elastic", "mocQi9I2*s1C90eUZdnG")).options(
            request_timeout=20,
            retry_on_timeout=True,
            ignore_status=[400, 404]
        )
        self.doc_type = "loyal"
        self.music_file = os.path.join('data', 'qa_corpus.json')

    '''创建ES索引，确定分词类型'''
    def create_mapping(self):
        node_mappings = {
            "mappings": {
                "properties": {
                    "question": {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart",
                        "index": "true"
                    },
                    "answers": {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart",
                        "index": "true"
                    },
                }
            }
        }
        if self.es.indices.exists(index=self._index):
            print('loyal_data索引存在，即将删除')
            self.es.indices.delete(index=self._index)
        else:
            print('索引不存在！可以创建')
        res = self.es.indices.create(index=self._index, body=node_mappings)
        print(res)

    '''批量插入数据'''

    def insert_data_bulk(self, action_list):
        success, _ = bulk(self.es, action_list, index=self._index, raise_on_error=True, refresh=True)
        print("Performed {0} actions. _: {1}".format(success, _))


def init_ES():
    pie = ProcessIntoES()
    # 创建ES的index
    pie.create_mapping()
    start_time = time.time()
    index = 0
    count = 0
    action_list = []
    BULK_COUNT = 1000  # 每BULK_COUNT个句子一起插入到ES中

    for line in open(pie.music_file, encoding='utf-8'):
        if not line:
            continue
        item = json.loads(line)
        index += 1
        action = {
            "_index": pie._index,
            "_source": {
                "question": item['question'],
                "answers": '\n'.join(item['answers']),
            }
        }
        action_list.append(action)
        if index == BULK_COUNT:
            pie.insert_data_bulk(action_list=action_list)
            index = 0
            count += 1
            action_list.clear()
            end_time = time.time()
            print("Time Cost:{0}".format(end_time - start_time))
    if index > 0:
        pie.insert_data_bulk(action_list=action_list)


if __name__ == "__main__":
    # 将数据库插入到elasticsearch当中
    init_ES()

