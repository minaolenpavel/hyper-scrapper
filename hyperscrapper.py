from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import time

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

action = webdriver.ActionChains(driver)
action.move_by_offset(10, 20)
action.perform()

menus_list = driver.find_elements(By.CLASS_NAME, "item-menu_niveau1")
for e in menus_list:
    print(e.text)
    if e.text == "Récapitulatif des cours":
        try:
            e.click()
        except ElementClickInterceptedException:
            time.sleep(10)
            e.click()





#recap_cours = By.
#
#recap_cours.click()

