from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
import time
import datetime
import random
import os


def week_number():
    week_num = datetime.date.today().strftime("%V")
    return week_num

def set_up_page(driver):
    time.sleep(3)
    menus = driver.find_elements(By.CLASS_NAME, "menu-principal_niveau1")
    menus = menus[4]
    action = webdriver.ActionChains(driver)
    action.move_to_element(menus)
    action.perform()
    action.move_by_offset(-150, 0)
    action.perform()
    action.move_by_offset(0, 60)
    action.perform()
    action.click()
    action.perform()

def scrap_schedules(filieres:list):
    service = Service(executable_path=r"C:\Program Files (x86)\geckodriver.exe")
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()

    driver.get("https://planning.inalco.fr/public")
    
    set_up_page(driver)
    count = 0
    for filiere in filieres:
        search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit")))
        search_bar.clear()
        search_bar.send_keys(filiere)
        time.sleep(0.5)
        search_bar.send_keys(Keys.ENTER)
        time.sleep(1)
        weeks = driver.find_elements(By.CLASS_NAME, "Calendrier_Jour_Const")
        for week in weeks:
            if week.text == "38":
                try:
                    week.click()
                except ElementClickInterceptedException:
                    try:
                        time.sleep(3)
                        week.click()
                    except:
                        print("extreme was triggered")
                        error_popup(driver)
                        for letter in filiere:
                            search_bar.send_keys(letter)
                            time.sleep(random.random())
                            results = driver.find_element(By.ID, "GInterface.Instances[1].Instances[1]_ContenuScroll")
                            subresults = results.find_elements(By.XPATH, "./*")
                            found = False
                            for result in subresults:
                                try:
                                    if result.text == filiere:
                                        found = True
                                        result.click()
                                        break 
                                except:
                                    continue
                            if found:
                                break                    
                        time.sleep(1)
                        continue
                finally:
                    try:
                        div_week= driver.find_element(By.CLASS_NAME, "WhiteSpaceNormal")
                        subelements = div_week.find_elements(By.XPATH, "./*")
                        raw_course = []
                        for course in subelements:
                            raw_course.append(course.text)
                        into_txt(raw_course)
                    except NoSuchElementException:
                        continue
        if count >= 25:
            driver.refresh()
            count = 0
            set_up_page(driver)
        else:
            count += 1

def into_txt(raw:list):
    with open("raw.txt", "a", encoding="utf-8") as txt_file:
        txt_file.writelines(raw)
        txt_file.close()

def error_popup(driver):
    button = driver.find_element(By.TAG_NAME, "button")
    button.click()

if __name__ == "__main__":
    filieres = ['cftfc']
    scrap_schedules(filieres)