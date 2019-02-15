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
            while odvod_account > 0 and self.odvod[odvod_account, 1] <= max_amount:
                odvod_account -= 1
            if odvod_account < 0 or odvod_account == 0 and self.odvod[0, 1] <= max_amount:
                return True

            while privod_account < len(self.privod) - 1 and self.privod[privod_account, 1] >= max_amount:
                privod_account += 1
            if privod_account >= len(self.privod) or privod_account == len(self.privod) - 1 and self.privod[privod_account, 1] >= max_amount:
                return False

            sum_to_get_rid_of = self.odvod[odvod_account, 1] - max_amount
            sum_to_fill = max_amount - self.privod[privod_account, 1]

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
    def create_arrays(self, zustatek, odvod, privod, money):
        self.money = money
        odvod = np.c_[odvod, zustatek]
        self.odvod = odvod[odvod[:, 0].argsort()]
        privod = np.c_[privod, zustatek]
        self.privod = privod[privod[:, 0].argsort()]
        print(self.binary_search(min(zustatek), max(zustatek)))


# zustatek = np.array([6, 0, 0])
# odvod = np.array([1, 1, 1])
# privod = np.array([1, 1, 1])

zustatek = np.random.randint(1, 100, 10)
odvod = np.random.randint(1, 50, 10)
privod = np.random.randint(1, 50, 10)
money = np.random.randint(1, 100)

print(zustatek)
print(odvod)
print(privod)
print(money)


all = np.c_[zustatek, odvod, privod]
xd = Mince()
xd.create_arrays(zustatek, odvod, privod, money)
