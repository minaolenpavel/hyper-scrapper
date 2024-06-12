import filieres
import schedule_extracter
import schedule_scrapper


def main():
    promos = filieres.extract_filieres()
    schedule_scrapper.scrap_schedules(promos)
    print(schedule_extracter.extract(schedule_extracter.raw_from_txt("raw.txt")))

if __name__ == "__main__":
    main()