import numpy as np


# [hodnota, adresa peněz],
def create_arrays(all):
    all = all[all[:, 0].argsort()]
    odvod = np.c_[all[:, 1], np.arange(0, all.shape[0])]
    odvod = odvod[odvod[:, 0].argsort()]
    print(odvod)
    privod = np.c_[all[:, 2], np.arange(0, all.shape[0])]
    privod = privod[privod[:, 0].argsort()]
    print(privod)
    all = all[:, 0]
    print(all)
    numbers = np.arange(all[0], all[-1])
    print(numbers)





zustatek = np.array([6, 3, 0])
odvod = np.array([1, 2, 1])
privod = np.array([1, 3, 1])

all = np.c_[zustatek, odvod, privod]

create_arrays(all)

