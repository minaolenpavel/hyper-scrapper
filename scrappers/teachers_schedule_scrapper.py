from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException, TimeoutException
import time
import datetime
import random
import os
from LogManager import LogManager

logger = None

def week_number():
    week_num = datetime.date.today().strftime("%V")
    return week_num

def set_up_page(driver):
    search_teachers = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "GInterface.Instances[0].Instances[1]_Combo0")))
    search_teachers.click()
    menus = driver.find_elements(By.CLASS_NAME, "item-menu_niveau1")
    for e in menus:
        if e.text == "Emploi du temps":
            try:
                action = webdriver.ActionChains(driver)
                action.move_to_element(e)
                action.perform()
            except ElementClickInterceptedException:
                time.sleep(10)
                action = webdriver.ActionChains(driver)
                action.move_to_element(e)
                action.perform()
            finally:
                action.move_by_offset(0,60)
                action.perform()
                action.click()
                action.perform()
            break
    time.sleep(1)

def create_driver():
    service = Service(executable_path=r"C:\Program Files (x86)\geckodriver.exe")
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    driver = webdriver.Firefox(service=service, options=options)
    #driver.maximize_window()
    driver.get("https://planning.inalco.fr/public")
    return driver

def scrap_schedules(teachers:list, reparse:bool = False):
    driver = create_driver()
    set_up_page(driver)
    if not reparse:
        create_txt()
    count = 0
    for teacher in teachers:
        search_bar = WebDriverWait(driver, random.random()).until(
        EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit")))
        search_bar.clear()
        search_bar.send_keys(teacher)
        time.sleep(random.random())
        search_bar.send_keys(Keys.ENTER)
        time.sleep(1)
        weeks = driver.find_elements(By.CLASS_NAME, "Calendrier_Jour_Const")
        for week in weeks:
            if week.text == "38":
                try:
                    week.click()
                except ElementClickInterceptedException:
                    logger.write("ElementClickInterceptedException", f"Week {week.text}")
                    continue
                finally:
                    try:
                        contenu = WebDriverWait(driver, random.random()).until(
                            EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[7]_Contenu_0")))
                        contenu_child = contenu.find_element(By.TAG_NAME, "tbody")
                        courses = contenu_child.find_elements(By.XPATH, "./*")
                        for course in courses:
                            into_txt(course.text)
                    except TimeoutException:
                        logger.write("TimeoutException", teacher)
                        continue
                    except StaleElementReferenceException:
                        logger.write("StaleElementReferenceException", teacher)
                        write_unparsed(teacher)
                        continue
        if count >= 25:
            driver.refresh()
            count = 0
            set_up_page(driver)
        else:
            count += 1
    driver.quit()
    if not reparse:
        check_unparsed()

def create_txt():
    if os.path.exists("raw.txt"):
        os.remove("raw.txt")
    open("raw.txt", "x", encoding="utf-8").close()
    if os.path.exists("unparsed.txt"):
        os.remove("unparsed.txt")
    open("unparsed.txt", "x", encoding="utf-8").close()

def write_unparsed(unparsed: str):
    with open("unparsed.txt", "a", encoding="utf-8") as unparsed_txt:
        unparsed_txt.write(unparsed + "\n")

def check_unparsed():
    unparsed = []
    with open("unparsed.txt", "r", encoding="utf-8") as unparsed_txt:
        unparsed = [line.strip() for line in unparsed_txt if line.strip()]
    if unparsed:
        logger.write("INFO", "Reparsing unparsed entries")
        for teacher in unparsed:
            logger.write("REPARSING", teacher)
        scrap_schedules(unparsed, reparse=True)
    if os.path.exists("unparsed.txt"):
        os.remove("unparsed.txt")

def into_txt(raw: str):
    with open("raw.txt", "a", encoding="utf-8") as txt_file:
        txt_file.write(raw + "\n")

def retrieve_teachers(filepath: str):
    teachers = []
    with open(filepath, "r", encoding="utf-8") as teachers_txt:
        teachers = [line.strip() for line in teachers_txt if line.strip()]
    return teachers

if __name__ == "__main__":
    logger = LogManager("schedule_scrapper_logs.txt", program_name="SCHEDULE SCRAPPER")
    logger.start_logs()
    teachers = retrieve_teachers("teachers.txt")
    scrap_schedules(teachers)
    logger.finish_logs()

