import datetime
import locale
import re


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
    raw_info = ['lundi 18 septembre 2023\n    09h30 - 12h30 TALA520B - Traitement statistique de corpus <Traitement automatique des langues (TAL) M2> TAL parcours Ingénierie multilingue\n<Traitement automatique des langues (TAL) M2> TeTraDom : Technologies de la Traduction et Traitement des Donné LO.01 - VPI + PC rue de Lille Rue Lille\nCours filière\n    15h00 - 17h00 TALA331C - Logique Traitement automatique des langues (TAL) L3 7.02-informatique VP + HP PLC   Cours filière\nmardi 19 septembre 2023\n    10h30 - 12h30 TALA430A - Langages reguliers Traitement automatique des langues (TAL) M1 3.08 - TBI.VP + PC + HP PLC\nCours filière\nvendredi 22 septembre 2023\n    12h30 - 14h00 TALA230A - Introduction au traitement automatique des langues Traitement automatique des langues (TAL) L2 7.04-informatique VP + HP PLC   Cours filière', 'mardi 19 septembre 2023\n    14h00 - 16h00 Réunion     L2.06 rue de Lille Rue Lille\nRéunion\nmercredi 20 septembre 2023\n    09h00 - 12h00 TALA450B - Programmation et Projet encadre 1 M. DUPONT Yoann Traitement automatique des langues (TAL) M1    \nCours filière\n    13h30 - 15h30 TALA230B - Fonctionnement des ordis et initiation a la programmation   <Traitement automatique des langues (TAL) L2> groupe 1 7.04-informatique VP + HP PLC   Cours filière\n    15h30 - 17h30 TALA230B - Fonctionnement des ordis et initiation a la programmation   <Traitement automatique des langues (TAL) L2> groupe 2 7.04-informatique VP + HP PLC   Cours filière\njeudi 21 septembre 2023\n    09h00 - 12h00 TALA540A - Documents structures   <Traitement automatique des langues (TAL) M2> TAL parcours Ingénierie multilingue\n<Traitement automatique des langues (TAL) M2> TeTraDom : Technologies de la Traduction et Traitement des Donné LO.01 - VPI + PC rue de Lille Rue Lille\nCours filière']
    raw_info = format_list(raw_info)
    print(extract(raw_info))