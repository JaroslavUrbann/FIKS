import random
import os


def random_numbers(max_number, n_columns, n_rows):
    with open("randomNumbers.txt", "a") as file:
        file.write(str(n_rows) + "\n")
        for i in range(n_rows):
            row = random.sample(range(1, max_number), n_columns)
            file.write(str(" ".join(map(str, row))) + "\n")


def random_random_numbers(n_instances, max_number, n_columns, n_rows):
    os.remove("randomNumbers.txt")
    for i in range(n_instances):
        random_numbers(max_number, n_columns, n_rows)


random_random_numbers(2, 20, 3, 5)

