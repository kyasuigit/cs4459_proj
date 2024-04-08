from chord_consistent_hashing import ChordConsistentHash
import redis


class InventorySystem:
    def __init__(self, nodes):
        self.nodes = nodes
        self.chord = ChordConsistentHash(nodes)

    def add_item(self, item_name, quantity):
        node = self.chord.get_successor(item_name)

        redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)
        redis_instance.hset(node, item_name, quantity)

        return node

    def get_item_quantity(self, item_name):
        node = self.chord.get_node(item_name)
        redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)

        return redis_instance.hget(node, item_name)
