from chord_consistent_hashing import ChordConsistentHash
import redis


class InventorySystem:
    def __init__(self, node_num):
        self.redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.chord = ChordConsistentHash(node_num, self.redis_conn)
        self.num_nodes = node_num

    def add_item(self, item_name, quantity):
        self.chord.add_item(item_name, [item_name, quantity])

    def get_item_quantity(self, item_name):
        node = self.chord.get_item(item_name)
        node_as_string = str(node.decode('utf-8')) if node else "Not Found"
        return node_as_string
    
    def get_number_of_nodes(self):
        return self.num_nodes
    
    def change_chord_algorithm (self, new_node):
        self.chord = ChordConsistentHash(new_node, self.redis_conn)
        self.num_nodes = new_node

    def get_all_items(self, node_id):
        return self.chord.get_all_items(node_id)
    
    def add_new_node(self):
        self.chord.add_new_node()

    def delete_node(self):
        self.chord.remove_node()