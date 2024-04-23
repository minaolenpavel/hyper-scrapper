from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import string
import time
import re

#Options for the web browser
service = Service(executable_path=r"C:\Program Files (x86)\geckodriver.exe")
options = webdriver.FirefoxOptions()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
driver = webdriver.Firefox(service=service, options=options)
#Launch the app in full screen to avoid scroll view errors
driver.maximize_window()
#Driver goes to the webpage
driver.get("https://www.inalco.fr/annuaire-enseignement-recherche")
#Scrolls to the element, to avoid scroll view error
driver.execute_script("window.scrollBy(0, 550)")

#Waits for 5 seconds so the page has time to load all the elements
time.sleep(2)

#Defines cookies Decline button, and clicks on it, so the view is not obstructed
cookies = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'tarteaucitronAllDenied2' )))
cookies.click()

#Sets a list of letters to iterate over
letters = list(string.ascii_uppercase)
#Loads the page till the parent element we want is loaded
search_letters = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "inalco-teacher-result-block")))

#Iterates over the list of letters, excluding the letters that are not available
#Clicks on each letter, good base to extract the teachers info later on
for l in letters:
    current_l = WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.ID, l)))
    letter_class = current_l.get_attribute("class")
    current_l.click()
    if 'inalco-teacher-results disabled-letter' in letter_class:
        pass
    else:
        current_l.click()

webSurname = driver.find_elements(By.CLASS_NAME, "inalco-teacher-card__name")
webName = driver.find_elements(By.CLASS_NAME, "inalco-teacher-card__surname")
names = []
# Iterates over the list of web element and extracts the name and surnames, also checks if this is not empty
#x : surname ; y : name
for x,y in zip(webSurname, webName):
    if x.text != '' and y.text != '':
        names.append((x.text, y.text))
print(names)
