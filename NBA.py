from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from prettyprinter import pprint as pp

from tqdm import tqdm

from links import Links



def get_jogos(nav, link_fixtures):
    nav.get(link_fixtures)

    liga = nav.find_element(By.CLASS_NAME, 'heading__name').text

    #print(liga)

    matches = nav.find_elements(By.CLASS_NAME, 'event__match')
    matches = matches[0:45]
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
    return liga, matches_list
    

def get_table(nav, link_table):
    nav.get(link_table)

    tables = nav.find_elements(By.CLASS_NAME, 'tableWrapper')
    table_dict = {}
    for table in tables[:2]:
        times = table.find_elements(By.CLASS_NAME, 'ui-table__row  ')
        for time in times:
            name = time.find_element(By.CLASS_NAME, 'tableCellParticipant__name').text
            games = time.find_element(By.CLASS_NAME, 'table__cell--value').text
            pontos = time.find_element(By.CLASS_NAME, 'table__cell--totalPoints').text
            pontos_pro = pontos[0:4] #chance de quebrar no inicio da temporada
            pontos_re = pontos[5:]


            table_dict[name] = [games, pontos_pro, pontos_re]

        #    print(name)
        #    print(games)
        #    print(pontos)
        #pp(table_dict)
    return table_dict


def calcula_media_jogos(table, matches):
    #print(liga)
    for match in tqdm(matches):
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
    return matches

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=3')
    nav = Chrome(options=chrome_options)
    nav.implicitly_wait(10)
    link_fixtures = Links.basquete[0]
    link_table = Links.basquete[1]
    table = get_table(nav, link_table)
    liga, matches = get_jogos(nav, link_fixtures)
    return liga, calcula_media_jogos(nav,table, matches)
    


if __name__ == '__main__':
    liga, matches = main()
    print(liga)
    pp(matches)