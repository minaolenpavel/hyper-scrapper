from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
import time
import os



def extract_teachers():
    service = Service(executable_path=r"C:\Program Files (x86)\geckodriver.exe")
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()
    driver.get("https://planning.inalco.fr/public")

    search_teachers = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "GInterface.Instances[0].Instances[1]_Combo0")))
    search_teachers.click()

    search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GInterface.Instances[1].Instances[1].bouton_Edit")))
    search_bar.send_keys(Keys.ENTER)
    time.sleep(3)
    results_list = driver.find_element(By.ID, "GInterface.Instances[1].Instances[1]_ContenuScroll")
    num_blocks = 83
    professeurs_connus = []

    action = webdriver.ActionChains(driver)
    first_block = driver.find_element(By.ID, "GInterface.Instances[1].Instances[1]_bloc0")
    action.move_to_element(first_block)
    action.perform()

    for bloc in range(num_blocks+1):
        if bloc != 83:
            professeur = driver.find_element(By.ID, f"GInterface.Instances[1].Instances[1]_bloc{bloc}")
            filiereplus = driver.find_element(By.ID, f"GInterface.Instances[1].Instances[1]_bloc{bloc+1}")
            driver.execute_script("arguments[0].scrollIntoView();", filiereplus)
            new_prof = correct_hyphens(professeur.text.rstrip())
            professeurs_connus.append(new_prof)
            write_txt(new_prof)
        elif bloc == 83:
            professeur = driver.find_element(By.ID, f"GInterface.Instances[1].Instances[1]_bloc{bloc}")
            new_prof = correct_hyphens(professeur.text.rstrip())
            professeurs_connus.append(new_prof)
            write_txt(new_prof)
            driver.quit

    professeurs = []
    for professeur in professeurs_connus:
        new_prof = professeur.replace("\n", ", ")
        professeurs.append(new_prof)

    professeurs = ", ".join(professeurs)
    professeurs = professeurs.split(", ")

def correct_hyphens(teacher:str):
    teacher_corrected = ""
    if "‑" in teacher:
        teacher_corrected = teacher.replace("‑", "-")
    
    return teacher_corrected


def write_txt(teacher:str):
    if not os.path.exists("teachers.txt"):
        open("teachers.txt", "x")
    with open("teachers.txt", "a", encoding="utf-8") as teachers_txt:
        teachers_txt.write(teacher + "\n")
        teachers_txt.close()

if __name__ == "__main__":
    extract_teachers()