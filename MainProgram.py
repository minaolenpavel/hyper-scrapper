import filieres
import schedule_extracter
import schedule_scrapper
import time
import datetime


def main():
    start = time.time()
    schedule_scrapper.scrap_schedules()
    print(schedule_extracter.extract(schedule_extracter.raw_from_txt("raw.txt")))
    end = time.time()
    print(f"Time taken to run the code was {str(datetime.timedelta(seconds=end-start))}")

if __name__ == "__main__":
    main()