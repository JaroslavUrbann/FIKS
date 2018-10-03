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

m = 16
n = 3
sort = 4
M = m
N = n

print((m * (n - 4)) - (m - 1) * int((n - 4) / 2) + (m + 3) + int(m / 4) * 3 * 2)
print((N * M) - (((M - sort) * (N - 1) / 2) + (sort * N) - (sort - 1 + int((N - 1) / 4) * 6 + N)))

