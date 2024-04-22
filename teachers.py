from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import string

#Options for the web browser
service = Service(executable_path=r"C:\Program Files (x86)\geckodriver.exe")
options = webdriver.FirefoxOptions()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
driver = webdriver.Firefox(service=service, options=options)
#Driver goes to the webpage
driver.get("https://www.inalco.fr/annuaire-enseignement-recherche")
#Sets a list of letters to iterate over
letters = list(string.ascii_uppercase)
#Loads the page till the parent element we want is loaded
search_letters = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "inalco-teacher-result-block")))
#Scrolls to the element, to avoid scroll view error
driver.execute_script("window.scrollTo(0, 583)")
#Iterates over the list of letters, excluding the letters that are not available
#Clicks on each letter, good base to extract the teachers info later on
for l in letters:
    current_l = driver.find_element(By.ID, l)
    letter_class = current_l.get_attribute("class")
    current_l.click()
    if 'inalco-teacher-results disabled-letter' in letter_class:
        pass
    else:
        current_l.click()