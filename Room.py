class Room:
    def __init__(self, code:str):
        self.code = code
        self.schedule = {
            "lundi" : [],
            "mardi" : [],
            "mercredi" : [],
            "jeudi" : [],
            "vendredi" : [],
            "samedi" : []
        }        
    
    def add_schedule(self, day:str, times:str):
        self.schedule[day].append(times)
        self.sort_schedule()
    
    def sort_schedule(self):
        for day in self.schedule.values():
            day.sort()