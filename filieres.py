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

search_bar = WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit")))
search_bar.send_keys("Russe")
time.sleep(3)
results_list = driver.find_element(By.ID, "GInterface.Instances[1].Instances[1]_ContenuScroll")

filieres = results_list.find_elements(By.TAG_NAME, "li")
for filiere in filieres:
    print(filiere.text)