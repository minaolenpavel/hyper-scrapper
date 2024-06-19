from schedule_extracter import * 
from Room import *
import re 
import DatabaseManager

class RoomManager:
    def __init__(self, week:str):
        self.week_number = week
        self.ordered_rooms = []

    def create_schedule(self, room_test: list, day: str):
        pattern_room = r"[0-7]\.[0-3][0-9]" 
        # Check if the room code is correctly a room code and not a time frame
        if re.search(pattern_room, room_test[1]):
            room_code = room_test[1]
            # Check if the room already exists in the list
            for room in self.ordered_rooms:
                if room.code == room_code:
                    room.add_schedule(day, room_test[0])
                    return  # Exit the function once the room is found and updated
            # If room doesn't exist, create a new room and append it to the list
            new_room = Room(room_code)
            new_room.schedule[day].append(room_test[0])
            self.ordered_rooms.append(new_room)

    def sort_rooms(self):
        self.ordered_rooms = sorted(self.ordered_rooms, key=lambda r: r.code)

if __name__ == "__main__":
    rooms = extract(raw_from_txt("raw.txt"))
    roomanager = RoomManager("38")
    for key, value in rooms.items():
        for room in value:
            roomanager.create_schedule(room, key)
    roomanager.sort_rooms()
    db_manager = DatabaseManager.DatabaseManager(roomanager.week_number)
    for room in roomanager.ordered_rooms:
        db_manager.add_room(room)