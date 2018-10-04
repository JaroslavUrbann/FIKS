import random


class Node:
    def __init__(self, id, value):
        self.parentsid, self.id, self.value = id, id, value


def FindParent(node, nodes_list):
    if node.parentsid == node.id:
        return node.parentsid
    else:
        node.parentsid = FindParent(nodes_list[node.parentsid])
        return node.parentsid


def Process_cenzor(i, cenzorka):
    return Node(i, cenzorka)


def Process_queries(query, queries_list):
    queries_list[query[1]].append(query)



def Main(cenzor_list, queries_list, nodes_list, nodes_stack):
    for i in range(len(cenzor_list)):
        nodes_list.append(Process_cenzor(i, cenzor_list[i]))
        while nodes_stack and nodes_stack[-1].value <= nodes_list[i].value:
            nodes_stack.pop().parentsid = nodes_list[i].id
        nodes_stack.append(nodes_list[i])
        for q in range(len(queries_list[i])):
            queries_list[i][q].append(FindParent(nodes_list[queries_list[i][q][0]], nodes_list))


first_row = [10, 1]
test_cenzor = random.sample(range(100), first_row[0])
queries_list = [[] for i in range(first_row[0])]
test_query = [2, 4]
nodes_list = []
nodes_stack = []

print(test_cenzor)
print(test_query)
Process_queries(test_query, queries_list)
Main(test_cenzor, queries_list, nodes_list, nodes_stack)
print(queries_list)
