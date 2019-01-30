from datetime import timedelta
import datetime



def calendar():
    with open("in.txt", "w") as file:
        file.write("80000\n")
        for i in range(80000):
            date = datetime.date(2120, 8, 20) + timedelta(days=i)
            file.write(str(date.day) + " " + str(date.month) + " " + str(date.year) + "\n")

calendar()