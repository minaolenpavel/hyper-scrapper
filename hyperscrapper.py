from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import time
import datetime

service = Service(executable_path=r"C:\Program Files (x86)\geckodriver.exe")
options = webdriver.FirefoxOptions()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
driver = webdriver.Firefox(service=service, options=options)
driver.maximize_window()

driver.get("https://planning.inalco.fr/public")
check_search_teachers = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "GInterface.Instances[0].Instances[1]_Combo0")))
search_by_teacher = driver.find_element(By.ID, "GInterface.Instances[0].Instances[1]_Combo0")
search_by_teacher.click()

search_bar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit"))
)
search_bar.send_keys("Nouvel")
search_bar.send_keys(Keys.ENTER)

menus = driver.find_elements(By.CLASS_NAME, "item-menu_niveau1")
for e in menus:
    if e.text == "Emploi du temps":
        try:
            action = webdriver.ActionChains(driver)
            action.move_to_element(e)
            action.perform()
            submenus = driver.find_elements(By.CLASS_NAME, "item-menu_niveau2")
        except ElementClickInterceptedException:
            print("excepted")
            time.sleep(10)
            action = webdriver.ActionChains(driver)
            action.move_to_element(e)
            action.perform()
            submenus = driver.find_elements(By.CLASS_NAME, "item-menu_niveau2")
        finally:
            action.move_by_offset(0,60)
            action.perform()
            action.click()
            action.perform()
        break

weeknum = 38
time.sleep(1)
weeks = driver.find_elements(By.CLASS_NAME, "Calendrier_Jour_Const")
for week in weeks:
    try:
        week.click()
    except ElementClickInterceptedException:
        time.sleep(1)
        week.click()
    finally:
        pass
