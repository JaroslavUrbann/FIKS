import random
import os


class Node:
    def __init__(self, id, value):
        self.parentsid_higher, self.parentsid_lower, self.id, self.value = id, id, id, value


def FindParent_higher(node, nodes_list):
    if node.parentsid_higher == node.id:
        return node.parentsid_higher
    else:
        node.parentsid_higher = FindParent_higher(nodes_list[node.parentsid_higher], nodes_list)
        return node.parentsid_higher


def FindParent_lower(node, nodes_list):
    if node.parentsid_lower == node.id:
        return node.parentsid_lower
    else:
        node.parentsid_lower = FindParent_lower(nodes_list[node.parentsid_lower], nodes_list)
        return node.parentsid_lower


def Process_cenzor(i, cenzor):
    return Node(i, cenzor)


def Process_queries(query, queries_list, queries_index):
    queries_list[query[1]].append(query)
    queries_index.append(query[1])


def Main(cenzor_list, queries_list):
    nodes_list = []
    nodes_stack_higher = []
    nodes_stack_lower = []
    parity_list = []
    for i in range(len(cenzor_list)):
        nodes_list.append(Process_cenzor(i, cenzor_list[i]))
        while nodes_stack_higher and nodes_stack_higher[-1].value <= nodes_list[i].value:
            nodes_stack_higher.pop().parentsid_higher = nodes_list[i].id
            nodes_stack_higher.append(nodes_list[i])
        while nodes_stack_lower and nodes_stack_lower[-1].value <= nodes_list[i].value:
            nodes_stack_lower.pop().parentsid_lower = nodes_list[i].id
            nodes_stack_lower.append(nodes_list[i])
        for q in range(len(queries_list[i])):
            lowest_value_node_id = FindParent_higher(nodes_list[queries_list[i][q][0]], nodes_list)
            queries_list[i][q].append(nodes_list[lowest_value_node_id].value)
            queries_list[i][q].append(FindParent_higher(nodes_list[queries_list[i][q][0]], nodes_list))


def WriteIt(queries_list, queries_index):
    with open("output.txt", "a") as output:
        for i in range(len(queries_index)):
            query_to_write = queries_list[queries_index.pop()].pop()
            output.write(str(query_to_write[2]) + "\n")
            output.write(str(query_to_write[3]) + "\n")


def realShit():
    os.remove("output.txt")
    with open("input.txt", "r") as input:
        tasks = int(input.readline())
        for i in range(tasks):
            first_line = list(map(int, input.readline().split(" ")))
            cenzors_list = list(map(int, input.readline().split(" ")))
            queries_list = [[] for i in range(first_line[0])]
            queries_index = []
            for a in range(first_line[1]):
                Process_queries(list(map(int, input.readline().split(" "))), queries_list, queries_index)
            Main(cenzors_list, queries_list)
            WriteIt(queries_list, queries_index)
            print(str(tasks - i))


realShit()
# first_row = [10, 1]
# test_cenzor = random.sample(range(100), first_row[0])
# queries_list = [[] for i in range(first_row[0])]
# test_query = [2, 4]
#
# print(test_cenzor)
# print(test_query)
# Process_queries(test_query, queries_list)
# Main(test_cenzor, queries_list)
# print(queries_list)

