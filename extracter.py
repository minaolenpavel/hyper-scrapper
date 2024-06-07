import datetime
import locale
import re


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

pattern_room = r"[0-7]\.[0-3][0-9]"
for key, value_list in info_by_day.items():
    for value in value_list:
        match = re.search(pattern_room, value)
        if match:
            print(f"Match {match.group()}")
        else:
            print("no match")

pattern_time = r"[0-2][0-9]h[0-6][0-9] - [0-2][0-9]h[0-6][0-9]"
for key, value_list in info_by_day.items():
    for value in value_list:
        match = re.search(pattern_time, value)
        if match:
            print(f"Match {match.group()}")
        else:
            print("no match")


raw_info = {day:[] for day in days_of_week}
for key, value_list in info_by_day.items():
    for value in value_list:
        match_time = re.search(pattern_time, value)
        match_room = re.search(pattern_room, value)
        if match_time and match_room:
            raw_info[key].append((match_time.group(), match_room.group()))
print(raw_info)

