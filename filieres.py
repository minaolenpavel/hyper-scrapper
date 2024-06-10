from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
import time

service = Service(executable_path=r"C:\Program Files (x86)\geckodriver.exe")
options = webdriver.FirefoxOptions()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
driver = webdriver.Firefox(service=service, options=options)
driver.maximize_window()
driver.get("https://planning.inalco.fr/public")



search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit")))
search_bar.send_keys(Keys.ENTER)
time.sleep(3)
results_list = driver.find_element(By.ID, "GInterface.Instances[1].Instances[1]_ContenuScroll")
num_blocks = 33
filieres_connues = []

action = webdriver.ActionChains(driver)
first_block = driver.find_element(By.ID, "GInterface.Instances[1].Instances[1]_bloc0")
action.move_to_element(first_block)
action.perform()

for bloc in range(num_blocks+1):
    if bloc != 33:
        filiere = driver.find_element(By.ID, f"GInterface.Instances[1].Instances[1]_bloc{bloc}")
        filiereplus = driver.find_element(By.ID, f"GInterface.Instances[1].Instances[1]_bloc{bloc+1}")
        driver.execute_script("arguments[0].scrollIntoView();", filiereplus)
        print(filiere.text)
        filieres_connues.append(filiere.text)
    elif bloc == 33:
        filiere = driver.find_element(By.ID, f"GInterface.Instances[1].Instances[1]_bloc{bloc}")
        print(filiere.text)
        filieres_connues.append(filiere)
    elif bloc == 34:
        driver.quit
        print(filieres_connues)

