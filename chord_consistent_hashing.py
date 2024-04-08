import redis
import hashlib


class ChordConsistentHash:

    def __init__(self, nodes, num_nodes=5):
        self.num_nodes = num_nodes
        self.ring = {}
        self.sorted_keys = []
        self.finger_table = []

        if nodes:
            for node in nodes:
                self.add_node(node)

    def create_finger_table(self):
        self.finger_table = [None] * (2 ** self.num_nodes)

        for i in range(self.num_nodes):
            finger_key = (2 ** i) % (2 % self.num_nodes)
            self.finger_table[finger_key]  = self.get_successor(finger_key)

    def obtain_hash(self, key):
        key_str = str(key)
        return int(hashlib.sha1(key_str.encode()).hexdigest(), 16) % (2 ** self.num_nodes)

    def add_node(self, node):
        for i in range(2 ** self.num_nodes):
            key = self.obtain_hash(f"{node}-{i}")
            self.ring[key] = node
            self.sorted_keys.append(key)

        self.sorted_keys.sort()
        self.create_finger_table()

    def remove_node(self, node):
        for i in range(2 ** self.num_nodes):
            key = self.obtain_hash(f"{node}-{i}")
            del self.ring[key]
            self.sorted_keys.remove(key)

    def get_successor(self, key):
        if key in self.finger_table:
            return self.finger_table[key]

        hash_val = self.obtain_hash(key)
        for ring_key in self.sorted_keys:
            if hash_val < ring_key:
                return ring_key

        return self.sorted_keys[0]

    def get_node(self, key):
        if not self.ring:
            return None

        hash_val = self.obtain_hash(key)
        for ring_key in self.sorted_keys:
            if hash_val < ring_key:
                return self.ring[ring_key]

        return self.sorted_keys[0]
