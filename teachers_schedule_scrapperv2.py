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
    

def scrap_schedules(filieres:list):
    service = Service(executable_path=r"C:\Program Files (x86)\geckodriver.exe")
    options = webdriver.FirefoxOptions()
    #options.add_argument("--headless")
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()

    driver.get("https://planning.inalco.fr/public")
    set_up_page(driver)
    
    if os.path.exists("raw.txt"):
        os.remove("raw.txt")
        open("raw.txt", "x")
    
    count = 0
    for filiere in filieres:
        search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit")))
        search_bar.clear()
        search_bar.send_keys(filiere)
        time.sleep(random.random())
        search_bar.send_keys(Keys.ENTER)
        time.sleep(1)
        weeks = driver.find_elements(By.CLASS_NAME, "Calendrier_Jour_Const")
        for week in weeks:
            if week.text == "38":
                try:
                    week.click()
                except ElementClickInterceptedException:
                    print("element click interception")
                    continue
                finally:
                    try:
                        contenu = WebDriverWait(driver, random.random()).until(EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[7]_Contenu_0")))
                        contenu_child = contenu.find_element(By.TAG_NAME, "tbody")
                        courses = contenu_child.find_elements(By.XPATH, "./*")
                        raw_course = []
                        for course in courses:
                            into_txt(course.text)
                    except TimeoutException:
                        print("time out")
                        print(filiere)
                        continue
                    except StaleElementReferenceException:
                        print("stale element")
                        print(filiere)                    
        if count >= 25:
            driver.refresh()
            count = 0
            set_up_page(driver)
        else:
            count += 1

def into_txt(raw:list):
    with open("raw.txt", "a", encoding="utf-8") as txt_file:
        txt_file.write(raw + "\n")
        txt_file.close()

def error_popup(driver):
    button = driver.find_element(By.TAG_NAME, "button")
    button.click()

if __name__ == "__main__":
    teachers = []
    with open("teachers.txt", "r", encoding="utf-8") as teachers_txt:
        for line in teachers_txt:
            teachers.append(line)
    scrap_schedules(teachers)

