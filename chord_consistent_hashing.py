import redis
import hashlib


class Node:
    def __init__(self, node_id, num_nodes, finger_table):
        self.node_id = node_id
        self.num_nodes = num_nodes
        self.finger_table = finger_table

    def obtain_hash(self, key):
        key_str = str(key)
        return int(hashlib.sha1(key_str.encode()).hexdigest(), 16) % (2 ** self.num_nodes)

class ChordConsistentHash:

    def __init__(self, num_nodes, redis_conn):
        self.num_nodes = num_nodes
        self.redis_conn = redis_conn
        self.nodes = [None] * (2**num_nodes)
        self.start_point = -1

        for i in range(1, num_nodes+1):
            hash_key = self.obtain_hash(i)
            self.add_node(hash_key)

            if i == 1:
                self.start_point = hash_key

        for i in range(1, num_nodes+1):
            hash_key = self.obtain_hash(i)
            self.nodes[hash_key].finger_table = self.create_finger_table(hash_key)

    def add_node(self, node_id):
        new_node = Node(node_id, self.num_nodes, None)
        self.nodes[int(node_id)] = new_node

    def obtain_hash(self, key):
        key_str = str(key)
        return int(hashlib.sha1(key_str.encode()).hexdigest(), 16) % (2 ** self.num_nodes)

    def create_finger_table(self, node_id):
        finger_table = []
        for i in range(self.num_nodes):
            finger_start = (node_id + 2**i) % (2 ** self.num_nodes)
            finger_succ = self.find_successor(finger_start)
            finger_table.append([finger_start, finger_succ])
        return finger_table

    def find_successor(self, key):
        successor = None

        for i in range(key, key + len(self.nodes)):
            if self.nodes[i % (2 ** self.num_nodes)]:
                successor = i % (2 ** self.num_nodes)
                break

        return successor

    def add_item(self, item_id, data):
        hash_key = self.obtain_hash(item_id)
        succesor_node = self.find_successor(hash_key)
        self.redis_conn.set(f"Chord_{succesor_node}_{hash_key}", data[1])

    def get_item(self, item_id):
        hashed_id = self.obtain_hash(item_id)

        def find_item(check_id):
            if self.redis_conn.exists(f"Chord_{check_id}_{hashed_id}"):
                return check_id
            for finger in self.nodes[check_id].finger_table:
                if self.redis_conn.exists(f"Chord_{finger[1]}_{hashed_id}"):
                    return find_item(finger[1])

        node_containing_item = find_item(self.start_point)
        return self.redis_conn.get(f"Chord_{node_containing_item}_{hashed_id}")

if __name__ == "__main__":
    chords = ChordConsistentHash(5)
    chords.add_item(13, "TEST")
    chords.add_item(54, "TESTASD")
    for x in chords.nodes:
        if x:
            print(x.node_id, x.items)


