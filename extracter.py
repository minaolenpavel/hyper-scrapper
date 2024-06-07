import datetime
import locale
import re
from dispoSalle import RoomAvailability

lines = []
with open("./extract.txt", "r") as extract:
    for l in extract:
        lines.append(l)

days_of_week = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
info_by_day = {day: [] for day in days_of_week}
current_day = None

for line in lines:
    for day in days_of_week:
        if day in line:
            current_day = day
            info_by_day[current_day].append(line)
            break
    else:
        if current_day is not None:
            info_by_day[current_day].append(line)

pattern = r"[0-2][0-9]h[0-6][0-9] - [0-2][0-9]h[0-6][0-9]"
for key, value_list in info_by_day.items():
    for value in value_list:
        match = re.search(pattern, value)
        if match:
            print(f"Match {match.group()}")
        else:
            print("no match")