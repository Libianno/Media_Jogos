from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from prettyprinter import pprint as pp

import tqdm as tqdm



def get_jogos(nav, link_fixtures):
    nav.get(link_fixtures)
    liga = nav.find_element(By.CLASS_NAME, 'event__title--type').text
    rodada = nav.find_element(By.CLASS_NAME, 'event__round').text

    #print(liga)
    #print(rodada)

    matches = nav.find_elements(By.CLASS_NAME, 'event__match')
    matches = matches[0:10]
    matches_list = []
    for match in matches:
        home = match.find_element(By.CLASS_NAME, 'event__participant--home').text
        away = match.find_element(By.CLASS_NAME, 'event__participant--away').text
        date = match.find_element(By.CLASS_NAME, 'event__time').text

        matches_list.append([home, away, date])
        
    #    print(home)
    #    print(away)
    #    print(date)
    #pp(matches_list)
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

    #    print(name)
    #    print(games)
    #    print(goals)
    #pp(table_dict)
    return table_dict

def calc(nav,link_table, link_fixtures):
    table = get_table(nav, link_table)
    liga, rodada, matches = get_jogos(nav, link_fixtures)
    #print(liga)
    #print(rodada)
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
    #pp(matches)
    return liga, rodada, matches

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=3')
    nav = Chrome(options=chrome_options)
    nav.implicitly_wait(10)
    links = [
    ['https://www.flashscore.com/football/england/premier-league/fixtures/',
    'https://www.flashscore.com/football/england/premier-league/standings/#/nunhS7Vn/table/overall'],#england
    ['https://www.flashscore.com/football/france/ligue-1/fixtures/',
    'https://www.flashscore.com/football/france/ligue-1/standings/#/zmkW5aIi/table/overall'],#frança 
    ['https://www.flashscore.com/football/germany/bundesliga/fixtures/',
    'https://www.flashscore.com/football/germany/bundesliga/standings/#/OIbxfZZI/table/overall'],#germany
    ['https://www.flashscore.com/football/italy/serie-a/fixtures/',
    'https://www.flashscore.com/football/italy/serie-a/standings/#/UcnjEEGS/table/overall'],#italy
    ['https://www.flashscore.com/football/netherlands/eredivisie/fixtures/',
    'https://www.flashscore.com/football/netherlands/eredivisie/standings/#/CfNLdj8j/table/overall'],#NETHERLANDS
    ['https://www.flashscore.com/football/spain/laliga/fixtures/',
    'https://www.flashscore.com/football/spain/laliga/standings/#/COQ6iu30/table/overall']#SPAIN
    ]
    for link in links:
        yield calc(nav, link[1], link[0])

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