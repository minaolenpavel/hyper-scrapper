from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


service = Service(executable_path=r"C:\Program Files (x86)\geckodriver.exe")
options = webdriver.FirefoxOptions()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
driver = webdriver.Firefox(service=service, options=options)

driver.get("https://planning.inalco.fr/public")
search_bar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit"))
)
search_bar.send_keys("russe")

one = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[1]_0"))
)
one.send_keys(Keys.ENTER)

