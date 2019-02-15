import numpy as np


class Mince:
    def binary_search(self, low, high):
        while low <= high:
            mid = int((low + high) / 2)
            is_possible = self.is_possible(mid)
            if mid == 0 and is_possible:
                return 0
            previous_is_possible = self.is_possible(mid-1)
            if is_possible and not previous_is_possible:
                return mid
            elif is_possible:
                high = mid - 1
            else:
                low = mid + 1
        print("what the frick")

    def is_possible(self, max_amount):
        money = self.money
        odvod_account = len(self.odvod) - 1
        privod_account = 0
        the_line = 0
        while money >= 0:
            while odvod_account > 0 and self.zustatky[self.odvod[odvod_account, 1]] <= max_amount:
                odvod_account -= 1
            if odvod_account == 0 and self.zustatky[self.odvod[odvod_account, 1]] <= max_amount:
                return True

            while privod_account < len(self.privod) - 1 and self.zustatky[self.privod[privod_account, 1]] >= max_amount:
                privod_account += 1
            if privod_account == len(self.privod) - 1 and self.zustatky[self.privod[privod_account, 1]] >= max_amount:
                return False

            sum_to_get_rid_of = self.zustatky[self.odvod[odvod_account, 1]] - max_amount
            sum_to_fill = max_amount - self.zustatky[self.privod[privod_account, 1]]

            if the_line > 0:
                sum_to_get_rid_of = the_line
            if the_line < 0:
                sum_to_fill = -the_line
            the_line = sum_to_get_rid_of - sum_to_fill

            price = sum_to_get_rid_of * (self.privod[privod_account, 0] + self.odvod[odvod_account, 0])
            if sum_to_fill > sum_to_get_rid_of:
                price = sum_to_get_rid_of * (self.privod[privod_account, 0] + self.odvod[odvod_account, 0])
                odvod_account -= 1
            if sum_to_fill < sum_to_get_rid_of:
                price = sum_to_fill * (self.privod[privod_account, 0] + self.odvod[odvod_account, 0])
                privod_account += 1
            if sum_to_fill == sum_to_get_rid_of:
                odvod_account -= 1
                privod_account += 1
            money -= price
        return False

    # [hodnota, adresa peněz],
    def create_arrays(self, all, money):
        self.money = money
        all = all[all[:, 0].argsort()]
        odvod = np.c_[all[:, 1], np.arange(0, all.shape[0])]
        self.odvod = odvod[odvod[:, 0].argsort()]
        privod = np.c_[all[:, 2], np.arange(0, all.shape[0])]
        self.privod = privod[privod[:, 0].argsort()]
        self.zustatky = all[:, 0]
        print(self.binary_search(self.zustatky[0], self.zustatky[-1]))


zustatek = np.array([3, 4, 2])
odvod = np.array([5, 5, 5])
privod = np.array([3, 3, 6])

money = 6

all = np.c_[zustatek, odvod, privod]
xd = Mince()
xd.create_arrays(all, money)

