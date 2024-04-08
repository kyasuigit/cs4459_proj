from chord_consistent_hashing import ChordConsistentHash
import redis


class InventorySystem:
    def __init__(self, node_num):
        self.redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.chord = ChordConsistentHash(node_num, self.redis_conn)

    def add_item(self, item_name, quantity):
        self.chord.add_item(item_name, [item_name, quantity])

    def get_item_quantity(self, item_name):
        node = self.chord.get_item(item_name)

        node_as_string = str(node.decode('utf-8')) if node else "Not Found"

        return node_as_string
