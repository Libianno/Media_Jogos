from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from prettyprinter import pprint as pp

import tqdm as tqdm

from links import Links


def get_jogos(nav, link_fixtures):
    nav.get(link_fixtures)
    liga = nav.find_element(By.CLASS_NAME, 'heading__name').text
    rodada = nav.find_element(By.CLASS_NAME, 'event__round').text
    matches = nav.find_elements(By.CLASS_NAME, 'event__match')
    matches = matches[0:10]
    matches_list = []
    for match in matches:
        home = match.find_element(By.CLASS_NAME, 'event__participant--home').text
        away = match.find_element(By.CLASS_NAME, 'event__participant--away').text
        date = match.find_element(By.CLASS_NAME, 'event__time').text

        matches_list.append([home, away, date])
    return liga, rodada, matches_list
    

def get_table(nav, link_table):
    nav.get(link_table)
    table = nav.find_element(By.CLASS_NAME, 'tableWrapper')
    times = table.find_elements(By.CLASS_NAME, 'ui-table__row  ')
    table_dict = {}
    for time in times:
        name = time.find_element(By.CLASS_NAME, 'tableCellParticipant__name').text
        games = time.find_element(By.CLASS_NAME, 'table__cell--value').text
        goals = time.find_element(By.CLASS_NAME, 'table__cell--score').text

        goals_pro = goals[0:2]
        goals_re = goals[3:]
        
        table_dict[name] = [games, goals_pro, goals_re]
    return table_dict

def calc(table, matches):
    for match in tqdm.tqdm(matches):
        games1 = table[match[0]][0]
        goals_pro1 = table[match[0]][1]
        goals_re1 = table[match[0]][2]

        games2 = table[match[1]][0]
        goals_pro2 = table[match[1]][1]
        goals_re2 = table[match[1]][2]

        means_of_match = (int(goals_pro1) + int(goals_pro2) + int(goals_re1) + int(goals_re2))/(int(games1) + int(games2)) 
        means_of_match = str(means_of_match)
        match.append(means_of_match[:4])
    return matches

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=3')
    nav = Chrome(options=chrome_options)
    nav.implicitly_wait(10)
    links = Links.futebol
    for link in links:
        table = get_table(nav, link[1])
        liga, rodada, matches = get_jogos(nav, link[0])
        yield liga, rodada, calc(nav, table, matches)

if __name__ == '__main__':
    run = main()
    try:
        while 1:
            liga, rodada, matches = next(run)
            print(liga)
            print(rodada)
            pp(matches)
    except StopIteration:
        pass