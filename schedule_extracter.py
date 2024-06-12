import datetime
import locale
import re


def format_list(raw_info:list):
    raw_info = " ".join(raw_info)
    pattern = r'\n| {3}'
    result_list = re.split(pattern, raw_info)
    result_list = [item.strip() for item in result_list if item.strip()] 
    return result_list

def extract(raw_schedule: list):
    # Define the days of the week
    days_of_week = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    # Initialize a dictionary to hold information by day, with empty lists for each day
    info_by_day = {day: [] for day in days_of_week}
    # Variable to keep track of the current day being processed
    current_day = None

    # Regular expression patterns to match room codes and time slots
    pattern_room = r"[0-7]\.[0-3][0-9]"  # Matches room codes like 5.29
    pattern_time = r"[0-2][0-9]h[0-6][0-9] - [0-2][0-9]h[0-6][0-9]"  # Matches time slots like 14h30 - 15h45
    
    # Iterate through each line in the raw schedule
    for line in raw_schedule:
        # Strip leading/trailing whitespace from the line
        line = line.strip()
        # Check if the line contains any day of the week, indicating a change in day
        for day in days_of_week:
            if day in line:
                current_day = day
                current_time = None  # Reset current time for the new day
                break
        # If we have identified a current day, proceed to extract time and room information
        if current_day:
            # Attempt to find a time slot in the line
            match_time = re.search(pattern_time, line)
            # Attempt to find a room code in the line
            match_room = re.search(pattern_room, line)
            # Skip processing if the line mentions "rue de Lille"
            if "rue de Lille" in line:
                continue  # Will skip all rooms in "rue de Lille"
            # If a time slot was found, store it
            if match_time:
                current_time = match_time.group()
            # If both a time slot and a room code were found, append them together
            if match_room and current_time:
                info_by_day[current_day].append((current_time, match_room.group()))
            # If only a room code was found, append it with a None time
            elif match_room: 
                info_by_day[current_day].append((None, match_room.group()))
            # If only a time slot was found, append it with a None room
            elif match_time:  
                info_by_day[current_day].append((match_time.group(), None))

    # After collecting all data, clean up the information by removing duplicate entries per day
    for day in info_by_day:
        clean_day_info = []
        last_time = None
        last_room = None
        # Iterate through the collected time and room pairs for the day
        for time, room in info_by_day[day]:
            # Update the last known time and room if they exist
            if time:
                last_time = time
            if room:
                last_room = room
            # If both time and room are set, add them to the cleaned-up list
            if last_time and last_room:
                clean_day_info.append((last_time, last_room))
                last_time = None
                last_room = None
        # Replace the original day's information with the cleaned-up version
        info_by_day[day] = clean_day_info

    # Return the cleaned-up information organized by day
    return info_by_day
    
if __name__ == "__main__":
    raw = ["lundi 18 septembre 2023\n    17h00 - 18h30 LETA110A - Grammaire lettone 1 <Diplôme de Langue et Civi 1 (autres langues)> Letton M. LE BOURHIS Eric 6.07-labo VP +PC - casques PLC\nCours\n    18h30 - 20h00 LETA110B - Étude de textes lettons 1 <Diplôme de Langue et Civi 1 (autres langues)> Letton M. LE BOURHIS Eric 6.07-labo VP +PC - casques PLC\nCours\nmardi 19 septembre 2023\n    13h30 - 15h00 ECOA130B - Sociétés et systèmes politiques comparés des États baltes 1 Estonien DLC1\nEstonien DLC2\nEstonien DLC3\nEstonien DLC4\nEstonien L1\nEstonien L2\nEstonien L3\nEstonien M1\nEstonien M2\nEurope Civ L1\nFinnois L1\nLetton L2\n<Diplôme de Langue et Civi 1 (autres langues)> Finnois\n<Diplôme de Langue et Civi 1 (autres langues)> Letton\n<Diplôme de Langue et Civi 2 (autres langues)> Letton Mme KESA Katerina 4.15 - TBI.VP (HDMI) + PC PLC\nCours Civi\n    16h30 - 17h30 Tutorat Europe Albanais L1\nBosniaque-Croate-Serbe L1\nEstonien L1\nEurope Civ L1\nFinnois L1\nGrec L1\nLituanien L1\nMacédonien L1\nPolonais L1\nRoumain L1\nSlovaque L1\nSlovène L1\nTchèque L1\nUkrainien L1 Mme DE BRISSON Louise 5.28 - TBI.VP + HP + PC PLC   Tutorat\nmercredi 20 septembre 2023\n    14h30 - 15h30 Tutorat Europe Estonien L1\nFinnois L1\nLituanien L1\nRoumain L1\nSlovène L1\n<Europe Civ L1> Tutorat civilisation régionale Mme REINALD Iris (Tutrice) 3.10 - TBI.VP PLC   Tutorat\n    15h30 - 17h00 ECOA130J - Histoire de la région baltique jusqu'au XIXè siècle Estonien DLC1\nEstonien DLC2\nEstonien DLC3\nEstonien DLC4\nEstonien L2\nEstonien L3\nEstonien M1\nEstonien M2\nFinnois L1\n<Diplôme de Langue et Civi 1 (autres langues)> Finnois\n<Europe Civ L1> Histoire de la région baltique\n<Diplôme de Langue et Civi 1 (autres langues)> Letton\n<Diplôme de Langue et Civi 2 (autres langues)> Letton Mme KESA Katerina\nM. LE BOURHIS Eric 5.22 - VPI (HDMI) + PC + HP PLC\nCours Civi\n    17h00 - 20h00 LETA110C - Pratique écrite et orale du letton 1 <Diplôme de Langue et Civi 1 (autres langues)> Letton Mme TROSCENKO Baiba 3.19 PLC\nCours\njeudi 21 septembre 2023\n    09h00 - 10h30 ECOA130A - Méthodologie : approches pluridisciplinaires de l'Europe 1 Albanais L1\nBosniaque-Croate-Serbe L1\nEstonien L1\nFinnois L1\nGrec L1\nHongrois L1\nLituanien L1\nMacédonien L1\nPolonais L1\nRoumain L1\nSlovaque L1\nUkrainien L1\n<Europe Civ L1> Gpe 1 Mme FOLSCHWEILLER Cécile\nM. LE BOURHIS Eric 3.08 - TBI.VP + PC + HP PLC\nCours Civi\n    11h00 - 12h30 ECOA130A - Méthodologie : approches pluridisciplinaires de l'Europe 1 Albanais L1\nBosniaque-Croate-Serbe L1\nEstonien L1\nGrec L1\nLituanien L1\nMacédonien L1\nRoumain L1\nSlovaque L1\nTchèque L1\n<Europe Civ L1> Gpe 2 Mme FOLSCHWEILLER Cécile\nM. LE BOURHIS Eric 5.05 - TBI.VP + PC + HP PLC\nCours Civi\n    17h00 - 18h30 LETA120B - Littérature lettone 1 <Diplôme de Langue et Civi 1 (autres langues)> Letton M. LE BOURHIS Eric 4.21 PLC\nCours\nvendredi 22 septembre 2023\n    13h00 - 14h30 ECOA130A - Méthodologie : approches pluridisciplinaires de l'Europe 1 Albanais L1\nBosniaque-Croate-Serbe L1\nBulgare L1\nEstonien L1\nGrec L1\nHongrois L1\nLituanien L1\nMacédonien L1\nRoumain L1\nSlovène L1\nTchèque L1\nUkrainien L1\n<Europe Civ L1> Gpe 3 Mme FOLSCHWEILLER Cécile\nM. LE BOURHIS Eric 3.13 VP + HP + PC PLC\nCours Civi", 'lundi 18 septembre 2023\n    16h00 - 19h00 LETA210C - Pratique écrite et orale du letton 3 <Diplôme de Langue et Civi 2 (autres langues)> Letton Mme ULME Madara 3.07 PLC\nCours\nmardi 19 septembre 2023\n    13h30 - 15h00 ECOA130B - Sociétés et systèmes politiques comparés des États baltes 1 Estonien DLC1\nEstonien DLC2\nEstonien DLC3\nEstonien DLC4\nEstonien L1\nEstonien L2\nEstonien L3\nEstonien M1\nEstonien M2\nEurope Civ L1\nFinnois L1\nLetton L1\n<Diplôme de Langue et Civi 1 (autres langues)> Finnois\n<Diplôme de Langue et Civi 1 (autres langues)> Letton\n<Diplôme de Langue et Civi 2 (autres langues)> Letton Mme KESA Katerina 4.15 - TBI.VP (HDMI) + PC PLC\nCours Civi\njeudi 21 septembre 2023\n    14h00 - 15h30 LETA210A - Grammaire lettone 3 <Diplôme de Langue et Civi 2 (autres langues)> Letton M. LE BOURHIS Eric 4.21 PLC\nCours\n    15h30 - 17h00 LETA210B - Étude de textes lettons 3 <Diplôme de Langue et Civi 2 (autres langues)> Letton Mme DE BRISSON Louise 4.21 PLC\nCours', 'mardi 19 septembre 2023\n    12h00 - 13h30 LETA310D - Letton des médias 1 Letton M1\n<Diplôme de Langue et Civi 3 (autres langues)> Letton Mme AUZINA Anda 6.12-labo PC- casques PLC\nCours\nmercredi 20 septembre 2023\n    17h30 - 19h00 LETA310A - Grammaire lettone 5 <Diplôme de Langue et Civi 3 (autres langues)> Letton M. LE BOURHIS Eric 4.08 PLC\nCours\njeudi 21 septembre 2023\n    17h00 - 18h30 LETA310B - Version lettone 1 Letton M1\nLetton M2\n<Diplôme de Langue et Civi 3 (autres langues)> Letton Mme TROSCENKO Baiba 5.14 PLC\nCours\n    18h30 - 20h00 LETA310A - Grammaire lettone 5 <Diplôme de Langue et Civi 3 (autres langues)> Letton M. LE BOURHIS Eric 4.21 PLC   Cours\n    20h00 - 21h30 LETA310C - Pratique écrite et orale du letton 5 <Diplôme de Langue et Civi 3 (autres langues)> Letton Mme ULME Madara 4.21 PLC\nCours']
    print(extract(raw))