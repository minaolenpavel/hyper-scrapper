import sqlite3
import json
from Room import Room

class DatabaseManager:
    def __init__(self, week_number:str) -> None:
        self.conn = sqlite3.connect("rooms.db")
        self.cursor = self.conn.cursor()
        table_name = f"Rooms_{week_number}"
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            code TEXT UNIQUE,
                            schedule TEXT
                            )
                            ''')
        self.conn.commit()

    def add_room(self, room:Room):
        self.cursor.execute(''' 
        INSERT INTO Rooms (code, schedule)
        VALUES (?,?)''', (room.code, room.to_dict()['schedule']))
        self.conn.commit()

if __name__ == "__main__":
    # Create an instance of DatabaseManager
    db_manager = DatabaseManager()

    # Create a Room object
    new_room = Room("5.25")
    new_room.add_schedule("lundi", '09h00 - 13h00')
    new_room.add_schedule("lundi", '14h00 - 15h00')

    # Add room to the database
    db_manager.add_room(new_room)

    # Retrieve room availability from the database
    #room_code_to_retrieve = "5.25"
    #retrieved_schedule = db_manager.retrieve_room_availability(room_code_to_retrieve)
    #if retrieved_schedule:
    #    print(f"Retrieved availability for room {room_code_to_retrieve}:")
    #    print(retrieved_schedule)
    #else:
    #    print(f"Failed to retrieve availability for room {room_code_to_retrieve}")
    ## Ensure proper closure of the database connection
    #del db_manager