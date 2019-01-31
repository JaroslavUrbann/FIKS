import fileinput
import sys


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

        # pocet gregorianskych prechodnych roku do zacatku noveho kalendare
        self.leap_years = self.y // 4 - self.y // 100 + self.y // 400 - (14 - self.m) // 12
        self.q = self.calculate_q()

        # vypocitani promenne pro funkci pro prevod z gregorianskeho kalendare do autoritarskeho dne
    def calculate_q(self):
        a = (14 - self.m) // 12
        m = self.m + 12 * a - 3
        return self.d + (153 * m + 2) // 5 - a * 365 - a // 4 + a // 100 - a // 400

    # prevod z gregorianskeho calendare do autoritarskeho dne na zaklade funkce pro prevod julianskeho dne dne
    def gregorian2authoritarian_day(self, d, m, y):
        a = (14 - m) // 12
        leap_years = y // 4 - y // 100 + y // 400
        if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0):
            leap_years -= a
        leap_years -= self.leap_years
        y = y - self.y - a
        m = m + 12 * a - 3
        return d + (153 * m + 2) // 5 + 365 * y + leap_years - self.q

    # prevod z autoritarskeho dne do autoritarskeho datumu
    def authoritarian_day2authoritarian(self, day):
        week = day % self.days_in_a_week + 1
        days_in_300 = (350*300) + 99
        year = day // days_in_300 * 300
        d = day % days_in_300
        days_in_3 = 3*350 + 1
        year += d // days_in_3 * 3
        leftover_days = d % days_in_3 + 1

        y = 0
        is_leap = (year + 1) % 3 == 0 and (year + 3) % 300 != 0
        calendar = self.year_calendar if (year + 1) % 3 != 0 or (year + 1) % 300 == 0 else self.leap_year_calendar
        if is_leap and leftover_days > 351:
            y += 1
            leftover_days -= 351
            calendar = self.year_calendar if (year + 2) % 3 != 0 or (year + 2) % 300 == 0 else self.leap_year_calendar
        elif not is_leap and leftover_days > 350:
            y += 1
            leftover_days -= 350
            calendar = self.year_calendar if (year + 2) % 3 != 0 or (year + 2) % 300 == 0 else self.leap_year_calendar
        is_leap = (year + 2) % 3 == 0 and (year + 3) % 300 != 0
        if is_leap and leftover_days > 351:
            y += 1
            leftover_days -= 351
            calendar = self.year_calendar if (year + 3) % 3 != 0 or (year + 3) % 300 == 0 else self.leap_year_calendar
        if not is_leap and leftover_days > 350:
            y += 1
            leftover_days -= 350
            calendar = self.year_calendar if (year + 3) % 3 != 0 or (year + 3) % 300 == 0 else self.leap_year_calendar

        days = leftover_days
        month = 1
        for m in calendar:
            if days - m < 1:
                break
            days -= m
            month += 1
        return str(week) + " " + str(days) + " " + str(month) + " " + str(year + y + 1)


if __name__ == "__main__":
    c = Converter()
    inp = fileinput.input()
    lines = int(inp.readline())
    for i in range(lines):
        date = list(map(int, inp.readline().split(" ")))
        day = c.gregorian2authoritarian_day(date[0], date[1], date[2])
        sys.stdout.write(c.authoritarian_day2authoritarian(day) + "\n")
