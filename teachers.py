from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import string

service = Service(executable_path=r"C:\Program Files (x86)\geckodriver.exe")
options = webdriver.FirefoxOptions()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
driver = webdriver.Firefox(service=service, options=options)

driver.get("https://www.inalco.fr/annuaire-enseignement-recherche")

letters = list(string.ascii_uppercase)
search_letters = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "inalco-teacher-result-block")))

for l in letters:
    current_l = driver.find_element(By.ID, l)
    letter_class = current_l.get_attribute("class")
    if 'inalco-teacher-results disabled-letter' in letter_class:
        pass
    else:
        current_l.click()