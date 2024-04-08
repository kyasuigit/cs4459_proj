from chord_consistent_hashing import ChordConsistentHash
import redis


class InventorySystem:
    def __init__(self, node_num):
        self.chord = ChordConsistentHash(node_num)

    def add_item(self, item_name, quantity):
        node = self.chord.add_item(item_name, quantity)

    def get_item_quantity(self, item_name):
        node = self.chord.get_item(item_name)

        return node
