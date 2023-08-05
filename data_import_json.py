import json
from py2neo import Graph, Node, Relationship, NodeMatcher


def get_graph():
    """
    connect the neo4j
    :return: neo4j object
    """
    try:
        graph = Graph("bolt://localhost:7687", username='neo4j', password='123456')
        print("success for neo4j connection.")
        return graph
    except Exception as e:
        print(e)
        return None


def deal_json(file_name):
    """
    deal with the json
    :param file_name: json file name
    :return: list abound with dicts
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
        # necessarily, the beginning of file is an illegal character for utf-8
        if content.startswith(u'\ufeff'):
            content = content.encode('utf8')[3:].decode('utf8')
        # add other deal steps
        content = str(content).replace('	', '')
        load_dict = json.loads(content)
    return load_dict


def trans_nodes(graph, file_name):
    """
    transfer the nodes to new db
    :param graph: neo4j object
    :param file_name: json file name
    :return: None
    """
    load_dict = deal_json(file_name)
    for row in load_dict:
        # select by json structure
        old_id = row['n']['identity']
        node_type = row['n']['labels'][0]
        properties = row['n']['properties']
        node = Node(node_type, old_id=old_id)
        for key, val in properties.items():
            node[key] = val
        print('creating-', node)
        graph.create(node)


def trans_relations(graph, file_name):
    """
    transfer the relations to the new db
    :param graph: neo4j object
    :param file_name: json file name
    :return: None
    """
    load_dict = deal_json(file_name)
    mather = NodeMatcher(graph)
    index = 1
    for row in load_dict:
        start_id = row['p']['segments'][0]['start']['identity']
        start_label = row['p']['segments'][0]['start']['labels'][0]
        end_id = row['p']['segments'][0]['end']['identity']
        end_label = row['p']['segments'][0]['end']['labels'][0]
        relation_type = row['p']['segments'][0]['relationship']['type']
        start_node = mather.match(start_label, old_id=start_id).first()
        end_node = mather.match(end_label, old_id=end_id).first()
        relation = Relationship(start_node, relation_type, end_node)
        print('inserting ' + str(index) + '-', relation)
        index += 1
        graph.create(relation)


if __name__ == '__main__':
    graph = get_graph()
    graph.delete_all()
    trans_nodes(graph, './records_nodes.json')
    trans_relations(graph, 'data/kg_loyal.json')
    # delete old id
    graph.run('MATCH (n) REMOVE n.old_id')
