from salle import Room

class RoomManager:
    def __init__(self) -> None:
        self.Rooms = []
    
    def add_room(self, newRoom:Room):
        if self.check_Rooms:
            pass
        else:
            pass
    
    def check_Rooms(self, roomNumber:str):
        for room in self.Rooms:
            if room.Number == roomNumber:
                return False
        return True