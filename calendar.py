import fileinput
import sys
import datetime


class Converter:
    def __init__(self):
        self.d = 20
        self.m = 8
        self.y = 1984

        self.first_leap_day = 767
        self.leap_day_interval = 1051
        self.year_calendar = [25, 21, 21, 24, 24, 25, 25, 21, 25, 24, 21, 24, 21, 24, 25]
        self.leap_year_calendar = [25, 21, 22, 24, 24, 25, 25, 21, 25, 24, 21, 24, 21, 24, 25]
        self.days_in_a_year = sum(self.year_calendar)
        self.days_in_a_week = 9

        # počet gregoriánských přechodných roků do začátku nového kalendáře
        self.leap_years = self.y // 4 - self.y // 100 + self.y // 400 - (14 - self.m) // 12
        self.q = self.calculate_q()

        # vypočítání proměnné pro funkci pro převod z gregoriánského kalendáře do autoritářského dne
    def calculate_q(self):
        a = (14 - self.m) // 12
        m = self.m + 12 * a - 3
        return self.d + (153 * m + 2) // 5 - a * 365 - a // 4 + a // 100 - a // 400

    # převod z gregoriánského kalendáře do autoritářského dne na základě funkce pro převod do juliánského dne
    def gregorian2authoritarian_day(self, d, m, y):
        a = (14 - m) // 12
        leap_years = y // 4 - y // 100 + y // 400
        if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0):
            leap_years -= a
        leap_years -= self.leap_years
        y = y - self.y - a
        m = m + 12 * a - 3
        return d + (153 * m + 2) // 5 + 365 * y + leap_years - self.q

    # převod z autoritářského dne do autoritářského datumu
    def authoritarian_day2authoritarian(self, day):
        origo = day
        week_day = day % self.days_in_a_week + 1
        calendar = self.year_calendar
        if day >= self.first_leap_day:
            day -= self.first_leap_day
            n_leap_years = day // self.leap_day_interval + 1
            non_leap = 0
            if day >= 99 * 1051:
                non_leap = day // (100 * 1051) + 1
            n_years = 3 * n_leap_years
            n_days_over = day % self.leap_day_interval + 67
            print(n_days_over)
            print((origo-n_leap_years+non_leap)% 350)
            if n_days_over > self.days_in_a_year or n_leap_years % 100 == 0:
                if n_leap_years % 100 != 0:
                    n_days_over -= 1
                days = n_days_over % self.days_in_a_year + 1
                n_years_over = n_days_over // self.days_in_a_year
            else:
                calendar = self.leap_year_calendar
                n_years_over = 0
                days = n_days_over + 1
            years = n_years + n_years_over
        else:
            years = day // self.days_in_a_year + 1
            days = day % self.days_in_a_year + 1

        month = 1
        for m in calendar:
            if days - m < 1:
                break
            days -= m
            month += 1

        return str(week_day) + " " + str(days) + " " + str(month) + " " + str(years)

    def final(self, day):
        day -= 767 + 99 * 1051
        non_leap_periods = max(0, day // (100 * 1051))
        years = 300 * non_leap_periods
        leftover_days = day % (100 * 1051)

        leap_periods = leftover_days // 1051
        more_years = 3 * leap_periods
        leftover_leftover_days = leftover_days % 1051

        more_more_years = 0
        leftover_leftover_leftover_days = leftover_leftover_days
        calendar = self.leap_year_calendar

        if leftover_leftover_days > 350:
            leftover_leftover_days -= 1
            more_more_years = leftover_leftover_days // 350
            leftover_leftover_leftover_days = leftover_leftover_days % 350
            calendar = self.year_calendar

        days = leftover_leftover_leftover_days + 1
        month = 1
        for m in calendar:
            if days - m < 1:
                break
            days -= m
            month += 1

        print(years)
        print(str(days) + " " + str(month) + " " + str(years + more_years + more_more_years))

    def too_much(self, day):
        days_in_300 = (350*300) + 99
        year = day // days_in_300 * 300
        d = day % days_in_300
        days_in_3 = 3*350 + 1
        year += d // days_in_3 * 3
        leftover_days = d % days_in_3 + 1
        # print(leftover_days)
        y = 0
        is_leap = (year + 1) % 3 == 0 and (year + 3) % 300 != 0
        calendar = self.year_calendar if (year + 1) % 3 != 0 or (year + 1) % 300 == 0 else self.leap_year_calendar

        if is_leap and leftover_days > 351:
            # print("1")
            y += 1
            leftover_days -= 351
            calendar = self.year_calendar if (year + 2) % 3 != 0 or (year + 2) % 300 == 0 else self.leap_year_calendar
        elif not is_leap and leftover_days > 350:
            y += 1
            # print("2")
            leftover_days -= 350
            calendar = self.year_calendar if (year + 2) % 3 != 0 or (year + 2) % 300 == 0 else self.leap_year_calendar
        is_leap = (year + 2) % 3 == 0 and (year + 3) % 300 != 0
        if is_leap and leftover_days > 351:
            y += 1
            # print("3")
            leftover_days -= 351
            calendar = self.year_calendar if (year + 3) % 3 != 0 or (year + 3) % 300 == 0 else self.leap_year_calendar
        if not is_leap and leftover_days > 350:
            y += 1
            # print("4")
            leftover_days -= 350
            calendar = self.year_calendar if (year + 3) % 3 != 0 or (year + 3) % 300 == 0 else self.leap_year_calendar

        days = leftover_days
        # print(days)
        month = 1
        # print(calendar)
        for m in calendar:
            if days - m < 1:
                break
            days -= m
            month += 1
        return str(days) + " " + str(month) + " " + str(year + y + 1)


if __name__ == "__main__":
    c = Converter()
    for line in fileinput.input():
        if not fileinput.isfirstline():
            date = list(map(int, line.split(" ")))
            day = c.gregorian2authoritarian_day(date[0], date[1], date[2])
            sys.stdout.write(c.too_much(day) + "\n")
    # day = c.gregorian2authoritarian_day(30, 8, 1984)
    # day = ((350*300) + 99)*2
    # print(c.too_much(day))

# 767 + 99*1051