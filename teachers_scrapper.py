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
import regex

def extract_teachers_list():
    #Options for the web browser
    service = Service(executable_path=r"C:\Program Files (x86)\geckodriver.exe")
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
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
    #cookies = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'tarteaucitronAllDenied2' )))
    #cookies.click()
    #Sets a list of letters to iterate over
    letters = list(string.ascii_uppercase)
    #Loads the page till the parent element we want is loaded
    search_letters = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inalco-teacher-result-block")))

    #Appends another Z so the names with this letter are not skipped
    letters.append('Z')
    #Iterates over the list of letters, excluding the letters that are not available
    #Clicks on each letter, good base to extract the teachers info later on
    teachers = []
    for l in letters:
        webSurname = driver.find_elements(By.CLASS_NAME, "inalco-teacher-card__name")
        webName = driver.find_elements(By.CLASS_NAME, "inalco-teacher-card__surname")
        # Iterates over the list of web element and extracts the name and surnames, also checks if this is not empty
        #x : surname ; y : name
        for x,y in zip(webSurname, webName):
            if x.text != '' and y.text != '':
                teachers.append(" ".join((x.text, y.text)))
        current_l = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, l)))
        letter_class = current_l.get_attribute("class")
        current_l.click()
        if 'inalco-teacher-results disabled-letter' in letter_class:
            pass
        else:
            current_l.click()
    driver.close()

    teachers = remove_non_latin(teachers)
    teachers = handle_exceptions(teachers)

    return teachers

def remove_non_latin(teachers:list):
    pattern = r'[^\p{Latin}^ -]'
    for teacher in teachers:
        index = teachers.index(teacher)
        new_name = regex.sub(pattern, '', teacher)
        teachers[index] = new_name
    return teachers

def handle_exceptions(teachers:list):
    index = teachers.index("BILOS Piotr (Pierre)")
    teachers[index] = "BILOS Piotr"
    index = teachers.index("CALZOLARI BOUVIER Valentina")
    teachers[index] = "CALZOLARI Valentina"
    index = teachers.index("BOUCHER Line")
    teachers[index] = "BOUCHER Lin Tran"
    index = teachers.index("CAPDEVILLE-ZENG Catherine")
    teachers[index] = "CAPDEVILLE Catherine"
    index = teachers.index("DEBSI Augustin Théodore")
    teachers[index] = "DEBSI Augustin"
    index = teachers.index("DURAND-DASTÈS Vincent")
    teachers[index] = "DURAND DASTES Vincent"
    index = teachers.index("EGLINGER Jean-Philippe")
    teachers[index] = "EGLINGER Jean - Philippe"
    index = teachers.index("GUERIN Mathieu")
    teachers.pop(index)
    index = teachers.index("GUILLARD Kahina")
    teachers.pop(index)
    index = teachers.index("NAÏT ZERAD Kamal")
    teachers[index] = "NAIT-ZERRAD Kamal"
    index = teachers.index('MOHAMED Oumrati')
    teachers.pop(index)
    index = teachers.index('NEUVE-EGLISE Amelie')
    teachers[index] = 'NEUVE - EGLISE Amelie'
    index = teachers.index('SAMSON NORMAND DE CHAMBOURG Dominique')
    teachers[index] = 'SAMSON Dominique'
    index = teachers.index("YAYA MCKENZIE Isabel")
    teachers[index] = "YAYA Isabel"
    index = teachers.index('YU Xinyue Cécilia')
    teachers[index] = "YU Xinyue"
    return teachers



if __name__ == "__main__":
    print(remove_non_latin(['ALLÈS Delphine', 'ALMENDROS Rubén', 'ANTONOV Anton', 'ARGUILLERE Stephane', 'ARMIANOV Gueorgui', 'ARSLANGUL Arnaud', 'AYKURT-BUCHWALTER Sulun', 'AYOUB Rania', 'ALLÈS Delphine', 'ALMENDROS Rubén', 'ANTONOV Anton', 'ARGUILLERE Stephane', 'ARMIANOV Gueorgui', 'ARSLANGUL Arnaud', 'AYKURT-BUCHWALTER Sulun', 'AYOUB Rania', 'BARONTINI Alexandrine', 'BAYOU Celine', 'BAZANTAY Jean', 'BERNITSKAIA Natalia', 'BILOS Piotr', 'BOIN PRINCIPATO Nicolas', 'BOUCHER Lin Tran', 'CHO Yunhaeng', 'CALZOLARI Valentina', 'CAPDEVILLE Catherine', 'CARANDINA Elisa', 'CARAYOL Martin', 'CASPILLO Nanette', 'CHALVIN Antoine', 'CHASSAING Sylvia', 'CHEIKH Mériam', 'CHIABOTTI Francesco', 'CHOI Jiyoung', 'CHOSSON Marie', 'COMOLLI Nadia', 'CORDOVA Johanna', 'COUMEL Laurent', 'COUSQUER David', 'DELAMOTTE Anne-Guibourg', 'DAO Huy Linh', 'DEBSI Augustin', 'DEWEL Serge', 'DIOT Benedicte', 'DOAN Cam Thi', 'DONABEDIAN-DEMOPOULOS Anaïd', 'DURAND DASTES Vincent', 'DUVALLON Outi', 'DUVIGNEAU Julie', 'DE PABLO Elisabeth', 'EBERSOLT Simon', 'EGLINGER Jean - Philippe', 'ELIAS Nicolas', 'FEDIUNIN Jules Sergei', 'FERKAL Masin', 'FOLSCHWEILLER Cecile', 'FORLOT Gilles', 'GODEFROY Noémi', 'GUETTA Alessandro', 'GUIDI Andreas', 'HAQUE Shahzaman', 'HURPEAU FUJIOKA Ami', 'INTHANO Theeraphong', 'JAFARI (ALAVI) Belgheis', 'JOMIER Augustin', 'KIM 金 Daeyeol 大烈', 'KESA Katerina', 'KONUMA Isabelle', 'LI Buqian 李不愆', 'LAGUER Hanane', 'LARIBI Soraya', 'LAVOIX Valérie', 'LE BOURHIS Eric', 'LIPMAN Ada', 'LÉGLISE Isabelle', 'MARDALE Alexandru', 'MACALUSO Ilenia', 'MADELAIN Anne', 'MAHIEU Marc-Antoine', 'MARCHINA Charlotte', 'MEROLLA Daniela', 'MEYER Ronny', 'MIKHEL Polina', 'MILOSAVLJEVIC Nenad', 'MOHAMED Oumrati', 'MORANGE Marianne', 'MUSSO Chloé', 'NAKAMURA-DELLOYE Yayoi', 'NAÏT ZERAD Kamal', 'NEUVE-EGLISE Amelie', 'NONDEDEO Philippe', 'NOUVEL Damien', 'NAKAMURA-DELLOYE Yayoi', 'NAÏT ZERAD Kamal', 'NEUVE-EGLISE Amelie', 'NONDEDEO Philippe', 'NOUVEL Damien', 'PEIGNÉ Céline', 'PEREGO Simon', 'PEREIRA Christophe', 'PÉRONNET Amandine', 'PEIGNÉ Céline', 'PEREGO Simon', 'PEREIRA Christophe', 'PÉRONNET Amandine', 'ROULOIS Alexandre', 'RUBINO Marcella', 'SAMSON NORMAND DE CHAMBOURG Dominique', 'SANGARÉ Youssouf', 'SALA Greta', 'SERFASS David', 'SIMONNEAU Damien', 'SLIM Assen', 'SMILAUER Ivan', 'STOCKINGER Peter', 'SULEYMANOV Murad', 'SZENDE Thomas', 'THOMANN Bernard', 'THUMELIN Claire', 'TOKUMITSU Naoko', 'TOUTANT Marc', 'THOMANN Bernard', 'THUMELIN Claire', 'TOKUMITSU Naoko', 'TOUTANT Marc', 'VALETTE Mathieu', 'VARGOVCIKOVA Jana', 'VASSILAKI Sophie', 'VERCUEIL Julien', 'VERON Emmanuel', 'VIGUIER Anne', 'VRINAT-NIKOLOV Marie', 'VUILLEUMIER Victor', 'WEI Lia', 'WEI Lia', 'YATZIV-MALIBERT Il-Il', 'YAYA MCKENZIE Isabel', 'YU Xinyue Cécilia', 'ZHANG Guochuan']))

