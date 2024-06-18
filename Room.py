from datetime import datetime

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

    def to_datetime(self, time_str: str):
        return datetime.strptime(time_str.replace('h', ':'), "%H:%M")

    def get_availability(self):
        availability = {}
        for day, intervals in self.schedule.items():
            start_dt = self.to_datetime("8h00")
            end_dt = self.to_datetime("22h00")
            # Sort the intervals by start time to ensure they are in chronological order
            intervals.sort(key=lambda x: self.to_datetime(x.split(" - ")[0]))
            # Initialize the current time to the start of the workday
            current_time = start_dt
            free_intervals = []
            for interval in intervals:
                # Split the interval into start and end times and convert them to datetime objects
                start, end = map(lambda x: self.to_datetime(x), interval.split(" - "))
                # If there's a gap before the current interval, add it to the free intervals
                if current_time < start:
                    free_intervals.append(f"{current_time.strftime('%Hh%M')} - {start.strftime('%Hh%M')}")
                # Update the current time to the end of the current interval
                current_time = end
            # After checking all intervals, if there's remaining time until the end of the workday, add it
            if current_time < end_dt:
                free_intervals.append(f"{current_time.strftime('%Hh%M')} - {end_dt.strftime('%Hh%M')}")
            availability[day] = free_intervals
        return availability



if __name__ == "__main__":
    new_room = Room("5.25") 
    new_room.add_schedule("lundi", '09h00 - 13h00')
    new_room.add_schedule("lundi", '14h00 - 15h00')
    print(new_room.get_availability())
