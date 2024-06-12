import re

days = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
raw = []
with open("raw.txt", "r") as raw_txt:
    info = raw_txt.readlines()
    raw.append(info)

info_by_day = {day: [] for day in days}

pattern_room = r"[0-7]\.[0-3][0-9]"  
pattern_time = r"[0-2][0-9]h[0-6][0-9] - [0-2][0-9]h[0-6][0-9]"
pattern = r"[0-2][0-9]h[0-6][0-9] - [0-2][0-9]h[0-6][0-9]|[0-7]\.[0-3][0-9]"

current_day = None
current_room = None
current_time = None
for info in raw:
    for sub in info:
        for day in days:
            if day in sub:
                current_day = day
                print(current_day)
        match = re.findall(pattern, sub)
        if len(match) == 2:
            info_by_day[current_day].append(match)
        elif len(match) == 1:
            for i in info_by_day[current_day]:
                if len(i) == 1:
                    i.append(match[0])
            else:
                info_by_day[current_day].append(match)


for day, timeslots in info_by_day.items():
    # Filter out sub-lists based on length and regex match
    filtered_timeslots = [timeslot for timeslot in timeslots if len(timeslot) > 1 and not re.match(pattern_room, timeslot[0])]
    
    # Update the day's timeslots with the filtered list
    info_by_day[day] = filtered_timeslots

print(info_by_day)