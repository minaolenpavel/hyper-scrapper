import datetime
import locale
import re
import schedule_scrapper
import teachers_scrapper


def format_list(raw_info:list):
    raw_info = " ".join(raw_info)
    pattern = r'\n| {3}'
    result_list = re.split(pattern, raw_info)
    result_list = [item.strip() for item in result_list if item.strip()] 
    return result_list

def extract(raw_schedule:list):
    days_of_week = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    info_by_day = {day: [] for day in days_of_week}
    current_day = None

    pattern_room = r"[0-7]\.[0-3][0-9]"
    pattern_time = r"[0-2][0-9]h[0-6][0-9] - [0-2][0-9]h[0-6][0-9]"
    
    for line in raw_schedule:
        line = line.strip()
        for day in days_of_week:
            if day in line:
                current_day = day
                current_time = None 
                break
        if current_day:
            match_time = re.search(pattern_time, line)
            match_room = re.search(pattern_room, line)
            if "rue de Lille" in line:
                continue #will skip all rooms in rue de lille
            if match_time:
                current_time = match_time.group()
            if match_room and current_time:
                info_by_day[current_day].append((current_time, match_room.group()))
            elif match_room: 
                info_by_day[current_day].append((None, match_room.group()))
            elif match_time:  
                info_by_day[current_day].append((match_time.group(), None))

    for day in info_by_day:
        clean_day_info = []
        last_time = None
        last_room = None
        for time, room in info_by_day[day]:
            if time:
                last_time = time
            if room:
                last_room = room
            if last_time and last_room:
                clean_day_info.append((last_time, last_room))
                last_time = None
                last_room = None
        info_by_day[day] = clean_day_info

    return info_by_day
    
if __name__ == "__main__":
    test_variables = ['ALLÈS Delphine', 'ALMENDROS Rubén', 'ANTONOV Anton', 'ARGUILLERE Stephane', 'ARMIANOV Gueorgui', 'ARSLANGUL Arnaud', 'AYKURT-BUCHWALTER Sulun', 'AYOUB Rania', 'ALLÈS Delphine', 'ALMENDROS Rubén', 'ANTONOV Anton', 'ARGUILLERE Stephane', 'ARMIANOV Gueorgui', 'ARSLANGUL Arnaud', 'AYKURT-BUCHWALTER Sulun', 'AYOUB Rania', 'BARONTINI Alexandrine', 'BAYOU Celine', 'BAZANTAY Jean', 'BERNITSKAIA Natalia', 'BILOS Piotr', 'BOIN PRINCIPATO Nicolas', 'BOUCHER Lin Tran', 'CHO Yunhaeng', 'CALZOLARI Valentina', 'CAPDEVILLE Catherine', 'CARANDINA Elisa', 'CARAYOL Martin', 'CASPILLO Nanette', 'CHALVIN Antoine', 'CHASSAING Sylvia', 'CHEIKH Mériam', 'CHIABOTTI Francesco', 'CHOI Jiyoung', 'CHOSSON Marie', 'COMOLLI Nadia', 'CORDOVA Johanna', 'COUMEL Laurent', 'COUSQUER David', 'DELAMOTTE Guibourg', 'DAO Huy Linh', 'DEBSI Augustin', 'DEWEL Serge', 'DIOT Benedicte', 'DOAN Cam Thi', 'DONABEDIAN-DEMOPOULOS Anaïd', 'DURAND-DASTÈS Vincent', 'DUVALLON Outi', 'DUVIGNEAU Julie', 'DE PABLO Elisabeth', 'EBERSOLT Simon', 'EGLINGER Jean-Philippe', 'ELIAS Nicolas', 'FEDIUNIN Jules Sergei', 'FERKAL Masin', 'FOLSCHWEILLER Cecile', 'FORLOT Gilles', 'GODEFROY Noémi', 'GUERIN Mathieu', 'GUETTA Alessandro', 'GUIDI Andreas', 'GUILLARD Kahina', 'HAQUE Shahzaman', 'HURPEAU FUJIOKA Ami', 'INTHANO Theeraphong', 'JAFARI (ALAVI) Belgheis', 'JOMIER Augustin', 'KIM 金 Daeyeol 大烈', 'KESA Katerina', 'KONUMA Isabelle', 'LI Buqian 李不愆', 'LAGUER Hanane', 'LARIBI Soraya', 'LAVOIX Valérie', 'LE BOURHIS Eric', 'LIPMAN Ada', 'LÉGLISE Isabelle', 'MARDALE Alexandru', 'MACALUSO Ilenia', 'MADELAIN Anne', 'MAHIEU Marc-Antoine', 'MARCHINA Charlotte', 'MEROLLA Daniela', 'MEYER Ronny', 'MIKHEL Polina', 'MILOSAVLJEVIC Nenad', 'MOHAMED Oumrati', 'MORANGE Marianne', 'MUSSO Chloé', 'NAKAMURA-DELLOYE Yayoi', 'NAÏT ZERAD Kamal', 'NEUVE-EGLISE Amelie', 'NONDEDEO Philippe', 'NOUVEL Damien', 'NAKAMURA-DELLOYE Yayoi', 'NAÏT ZERAD Kamal', 'NEUVE-EGLISE Amelie', 'NONDEDEO Philippe', 'NOUVEL Damien', 'PEIGNÉ Céline', 'PEREGO Simon', 'PEREIRA Christophe', 'PÉRONNET Amandine', 'PEIGNÉ Céline', 'PEREGO Simon', 'PEREIRA Christophe', 'PÉRONNET Amandine', 'ROULOIS Alexandre', 'RUBINO Marcella', 'SAMSON NORMAND DE CHAMBOURG Dominique', 'SANGARÉ Youssouf', 'SALA Greta', 'SERFASS David', 'SIMONNEAU Damien', 'SLIM Assen', 'SMILAUER Ivan', 'STOCKINGER Peter', 'SULEYMANOV Murad', 'SZENDE Thomas', 'THOMANN Bernard', 'THUMELIN Claire', 'TOKUMITSU Naoko', 'TOUTANT Marc', 'THOMANN Bernard', 'THUMELIN Claire', 'TOKUMITSU Naoko', 'TOUTANT Marc', 'VALETTE Mathieu', 'VARGOVCIKOVA Jana', 'VASSILAKI Sophie', 'VERCUEIL Julien', 'VERON Emmanuel', 'VIGUIER Anne', 'VRINAT-NIKOLOV Marie', 'VUILLEUMIER Victor', 'WEI Lia', 'WEI Lia', 'YATZIV-MALIBERT Il-Il', 'YAYA MCKENZIE Isabel', 'YU Xinyue Cécilia', 'ZHANG Guochuan']
    raw_info = schedule_scrapper.extract_rooms(test_variables)
    raw_info = format_list(raw_info)
    print(extract(raw_info))