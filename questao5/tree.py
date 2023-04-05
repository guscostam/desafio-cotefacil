import unittest

# A classe Node representa um nó na árvore.
# Cada nó tem um valor e uma lista de filhos, que começa vazia.
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

# A classe Tree representa a árvore como um todo e recebe o nó raiz como parâmetro em seus construtor.
class Tree:
    def __init__(self, root):
        self.root = root

# Este teste cria uma árvore com seis nós e verifica se a ordem de visita dos nós durante a busca em profundidade está correta.
class TestTree(unittest.TestCase):
    def test_dfs(self):
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)
        node4 = Node(4)
        node5 = Node(5)
        node6 = Node(6)

        node1.children.append(node2)
        node2.children.append(node3)
        node3.children.append(node4)
        node4.children.append(node5)
        node5.children.append(node6)

        tree = Tree(node1)

        # Para percorrer a árvore, a busca em profundidade (DFS) será utilizada.
        result = []
        def dfs(node):
            result.append(node.value)
            for child in node.children:
                dfs(child)

        dfs(tree.root)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6])

if __name__ == '__main__':
    unittest.main()

