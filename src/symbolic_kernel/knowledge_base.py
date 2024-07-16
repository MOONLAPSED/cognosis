import json

class Node:
    def __init__(self, concept):
        self.concept = concept
        self.relations = {}

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, concept):
        if concept not in self.nodes:
            self.nodes[concept] = Node(concept)

    def add_relation(self, concept1, concept2, relation_type):
        self.add_node(concept1)
        self.add_node(concept2)
        self.nodes[concept1].relations[concept2] = relation_type

    def serialize(self):
        return json.dumps({c: {
            'concept': n.concept,
            'relations': n.relations
        } for c, n in self.nodes.items()})

    @classmethod
    def deserialize(cls, data):
        graph = cls()
        nodes_data = json.loads(data)
        for concept, node_data in nodes_data.items():
            graph.add_node(concept)
            for related_concept, relation in node_data['relations'].items():
                graph.add_relation(concept, related_concept, relation)
        return graph