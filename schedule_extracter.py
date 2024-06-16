import re

def raw_from_txt(filepath:str):
    raw = []
    with open(filepath, "r", encoding="utf-8") as raw_txt:
        info = raw_txt.readlines()
        raw.append(info)
    return raw

def extract(raw:list):
    days = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    info_by_day = {day: [] for day in days}
    pattern_room = r"[0-7]\.[0-3][0-9]"  
    pattern_time = r"[0-2][0-9]h[0-6][0-9] - [0-2][0-9]h[0-6][0-9]"
    pattern = r"[0-2][0-9]h[0-6][0-9] - [0-2][0-9]h[0-6][0-9]|[0-7]\.[0-3][0-9]"
    current_day = None
    for info in raw:
        for sub in info:
            for day in days:
                if day in sub:
                    current_day = day
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
        filtered_timeslots = []
        for timeslot in timeslots:
            # Filter out sub-lists based on length and regex match
            if len(timeslot) > 1 and not re.match(pattern_room, timeslot[0]):
                filtered_timeslots.append(timeslot)
            else:
                print(f"Filtered out: {timeslot}")  # Print filtered out items
        # Update the day's timeslots with the filtered list
        info_by_day[day] = filtered_timeslots

    with open('dict_output.txt', 'w') as file:
        file.write(str(info_by_day))

    return info_by_day

if __name__ == "__main__":
    raw = raw_from_txt("raw.txt")
    extract(raw)
