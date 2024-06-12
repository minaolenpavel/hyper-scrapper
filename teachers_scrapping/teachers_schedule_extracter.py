import datetime
import locale
import re
import teachers_schedule_scrapper
import teachers_scrapper

def format_list(raw_info:list):
    raw_info = " ".join(raw_info)
    pattern = r'\n| {3}'
    result_list = re.split(pattern, raw_info)
    result_list = [item.strip() for item in result_list if item.strip()] 
    return result_list

def extract(raw_schedule:list):
    days_of_week = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    info_by_day = {day: [] for day in days_of_week}
    current_day = None

    pattern_room = r"[0-7]\.[0-3][0-9]"
    pattern_time = r"[0-2][0-9]h[0-6][0-9] - [0-2][0-9]h[0-6][0-9]"
    
    for line in raw_schedule:
        line = line.strip()
        for day in days_of_week:
            if day in line:
                current_day = day
                current_time = None 
                break
        if current_day:
            match_time = re.search(pattern_time, line)
            match_room = re.search(pattern_room, line)
            if "rue de Lille" in line:
                continue #will skip all rooms in rue de lille
            if match_time:
                current_time = match_time.group()
            if match_room and current_time:
                info_by_day[current_day].append((current_time, match_room.group()))
            elif match_room: 
                info_by_day[current_day].append((None, match_room.group()))
            elif match_time:  
                info_by_day[current_day].append((match_time.group(), None))

    for day in info_by_day:
        clean_day_info = []
        last_time = None
        last_room = None
        for time, room in info_by_day[day]:
            if time:
                last_time = time
            if room:
                last_room = room
            if last_time and last_room:
                clean_day_info.append((last_time, last_room))
                last_time = None
                last_room = None
        info_by_day[day] = clean_day_info

    return info_by_day
    
if __name__ == "__main__":
    teachers = teachers_scrapper.extract_teachers_list()
    raw_info = teachers_schedule_scrapper.extract_rooms(teachers)
    raw_info = format_list(raw_info)
    print(extract(raw_info))