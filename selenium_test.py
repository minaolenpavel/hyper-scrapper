from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

service = Service(executable_path=r"C:\Program Files (x86)\geckodriver.exe")
options = webdriver.FirefoxOptions()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
driver = webdriver.Firefox(service=service, options=options)

driver.get("https://planning.inalco.fr/public")

search_bar = driver.find_element(By.TAG_NAME, 'input')
search_bar.send_keys("class1")
search_bar.send_keys(Keys.RETURN)