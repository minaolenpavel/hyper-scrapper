from scrappers.teachers_scrapper import *
from scrappers.teachers_schedule_scrapper import * 
from schedule_extracter import *
from RoomManager import *

def main():
    week = "38"
    teachers = extract_teachers()
    scrap_schedules(week, teachers)
    schedule = extract(raw_from_txt(f"raw{week}.txt"))
    roomanager = RoomManager(week)
    for key, value in schedule.items():
        for room in value:
            roomanager.create_schedule(room, key)
    roomanager.sort_rooms()
    db_manager = DatabaseManager.DatabaseManager(roomanager.week_number)
    for room in roomanager.ordered_rooms:
        db_manager.add_room(room)