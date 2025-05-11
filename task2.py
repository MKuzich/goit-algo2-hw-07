from functools import lru_cache
import matplotlib.pyplot as plt
import timeit
from tabulate import tabulate

@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.left_node = None
        self.right_node = None

class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert_node(data, self.root)

    def _insert_node(self, data, current_node):
        if data[0] < current_node.data[0]:
            if current_node.left_node:
                self._insert_node(data, current_node.left_node)
            else:
                current_node.left_node = Node(data, current_node)
        else:
            if current_node.right_node:
                self._insert_node(data, current_node.right_node)
            else:
                current_node.right_node = Node(data, current_node)

    def find(self, data):
        node = self.root
        while node is not None:
            if data < node.data:
                node = node.left_node
            elif data > node.data:
                node = node.right_node
            else:
                self._splay(node)
                return node.data
        return None

    def _splay(self, node):
        while node.parent is not None:
            if node.parent.parent is None:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left_node and node.parent == node.parent.parent.left_node:
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right_node and node.parent == node.parent.parent.right_node:
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else: 
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        left_child = node.left_node
        if left_child is None:
            return

        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node

        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child

        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        right_child = node.right_node
        if right_child is None:
            return

        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node

        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child

        right_child.left_node = node
        node.parent = right_child

def fibonacci_splay(n, tree):
    node = tree.root
    while node:
        node_n, node_val = node.data
        if n < node_n:
            node = node.left_node
        elif n > node_n:
            node = node.right_node
        else:
            tree._splay(node)
            return node_val

    if n < 2:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)

    tree.insert((n, result))
    return result

if __name__ == '__main__':
    
    fib_values = list(range(0, 951, 50))
    lru_times = []
    splay_times = []

    for n in fib_values:
        fibonacci_lru.cache_clear()
        lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=3) / 3
        lru_times.append(lru_time)

        splay_time = timeit.timeit(lambda: fibonacci_splay(n, SplayTree()), number=3) / 3
        splay_times.append(splay_time)

    plt.figure(figsize=(12, 6))
    plt.plot(fib_values, lru_times, label="LRU Cache", marker='o')
    plt.plot(fib_values, splay_times, label="Splay Tree", marker='s')
    plt.xlabel("Fibonacci Number (n)")
    plt.ylabel("Average Execution Time (seconds)")
    plt.title("Performance Comparison: LRU Cache vs. Splay Tree")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()\
    
    table = [(n, f"{lt:.6f}", f"{st:.6f}") for n, lt, st in zip(fib_values, lru_times, splay_times)]
    headers = ["n", "LRU Cache Time (s)", "Splay Tree Time (s)"]
    tabulated_output = tabulate(table, headers, tablefmt="grid")
    print(tabulated_output)