from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import time

def extract_rooms(teachers:list):
    service = Service(executable_path=r"C:\Program Files (x86)\geckodriver.exe")
    options = webdriver.FirefoxOptions()
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()

    driver.get("https://planning.inalco.fr/public")
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

    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit"))
    )
    raw_schedules = []
    for teacher in teachers:
        search_bar.send_keys(teacher)
        search_bar.send_keys(Keys.ENTER)

        time.sleep(1)
        weeks = driver.find_elements(By.CLASS_NAME, "Calendrier_Jour_Const")
        
        for week in weeks:
            if week.text == "38":
                try:
                    week.click()
                except ElementClickInterceptedException:
                    time.sleep(1)
                    week.click()
                finally:
                    div_week= driver.find_element(By.CLASS_NAME, "WhiteSpaceNormal")
                    subelements = div_week.find_elements(By.XPATH, "./*")
                    for course in subelements:
                        raw_schedules.append(course.text)
    
    return raw_schedules

if __name__ == "__main__":
    teachers = ['NOUVEL Damien', 'MAGISTRY Pierre']
    print(extract_rooms(teachers))