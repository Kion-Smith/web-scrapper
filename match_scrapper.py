from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
from bs4.element import Tag
from match_data import GameData

from player_stats import PlayerStats
BASE_URL = "https://tracker.gg"

compare_list = []

def get_inner_html_from_selenium(river:webdriver, element:WebElement):
    return driver.execute_script("return arguments[0].innerHTML;",element)

def get_links_for_a_day(driver:webdriver, game_data:WebElement) -> str:
    game_entry_info = get_inner_html_from_selenium(driver,game_data)
    return parse_match_entry(game_entry_info)

def parse_match_entry(games_data:str):
    match_links = []
    soup = BeautifulSoup(games_data,"html.parser")
    matches_lost =soup.find_all("div",{"class":"match match--lost"})
    matches_won =soup.find_all("div",{"class":"match match--won"})

    #print("lost",len(matches_lost),"and won",len(matches_won))
    for cur in matches_lost:
        match_links.append(cur.find("a",{"class":"match__link"})['href'])

    for cur in matches_won:
        match_links.append(cur.find("a",{"class":"match__link"})['href'])
        #parse_match_information(driver,cur)
    return match_links


def parse_match_information(driver:webdriver,match_link:str):
    #/valorant/match/1bf80379-415f-467d-9cb5-42140f4dcfcb?handle=Noik%23Neon
    #https://tracker.gg/valorant/match/341cb0f7-08f1-463b-82c1-f8e73b70d95b?handle=Noik%23Neon
    driver.get(BASE_URL+match_link)
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'trn-match-drawer__content'))
        WebDriverWait(driver, 10).until(element_present)
    except TimeoutException:
        print("Timed out waiting for match page to load")
    match_table = driver.find_element(By.CLASS_NAME,"trn-match-drawer")
    raw_match_page = get_inner_html_from_selenium(driver,match_table)
    match_page = BeautifulSoup(raw_match_page,"html.parser")
    team_one_score = match_page.find("div",{"class" :"trn-match-drawer__header-value valorant-color-team-1"}).getText()
    team_two_score= match_page.find("div",{"class" :"trn-match-drawer__header-value valorant-color-team-2"}).getText()
    map  = match_page.find("div",{"class":"trn-match-drawer__header-value"}).getText()
    date_time  = match_page.find("div",{"class":"trn-match-drawer__header-block vm-header-time"}).getText()
    
    players = match_page.find_all("div",{"class":"st-content__item"})
    players_team = []
    enemys_team =[]
    
    for i,cur in enumerate(players):
        player_stat = parse_player_information(cur)
        if i > 5:
            players_team.append(player_stat)
        else:
            enemys_team.append(player_stat)

    #print(team_one_score,team_two_score,map,date_time)
    game_info = GameData(team_one_score,team_two_score,map,date_time,players_team,enemys_team)
    game_info.to_string()

    temp_me =game_info.find_player_stats("Noik")
    temp_other = game_info.find_player_stats("zuviel")

    if temp_me and temp_other:
        print("Found")
        compare_list.append((temp_me,temp_other))

    #print(match_name.getText(),time_played.getText(),game_score,kda,kd,hs_percentage,adr,acs,match_link)
    #return match_link

def parse_player_information(player_info:Tag) -> PlayerStats:
    player_name = player_info.find("span",{"class":"trn-ign__username"}).getText()
    player_tag = player_info.find("span",{"class":"trn-ign__discriminator"}).getText()

    stats_data = player_info.find_all("div",{"class","st__item st-content__item-value st__item--align-center"})
    
    acs = stats_data[0].getText()
    kills = stats_data[1].getText()
    deaths = stats_data[2].getText()
    assists = stats_data[3].getText()
    
    if len(stats_data) == 12:
        kd = stats_data[4].getText()
        adr = stats_data[5].getText()
        hs = stats_data[6].getText().replace("%","")
        kast = stats_data[7].getText().replace("%","")
        fk = stats_data[8].getText()
        fd = stats_data[9].getText()
        mk = stats_data[10].getText()
        econ = stats_data[11].getText()
    else:
        kd = stats_data[5].getText()
        adr = stats_data[6].getText()
        hs = stats_data[7].getText().replace("%","")
        kast = stats_data[8].getText().replace("%","")
        fk = stats_data[9].getText()
        fd = stats_data[10].getText()
        mk = stats_data[11].getText()
        econ = stats_data[12].getText()

    player_stats = PlayerStats(player_name,player_tag,int(acs),int(kills),int(deaths),int(assists),int(kills)-int(deaths),float(kd),float(adr),int(hs),int(kast),int(fk),int(fd),int(mk),int(econ))
    return player_stats

def update_page(driver:webdriver,button):
    x = driver.execute_script("arguments[0].click();",button)
    #print(x)

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://tracker.gg/valorant/profile/riot/Noik%23Neon/matches?playlist=unrated")
#sleep(10)

try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'trn-gamereport-list'))
    WebDriverWait(driver, 10).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")

for i in range(10):
    x = driver.find_element(By.TAG_NAME,"button")
    update_page(driver,x)
    driver.implicitly_wait(5)

while True:
    games_in_a_day = driver.find_elements(By.CLASS_NAME,"trn-gamereport-list__group")
    try:
        load_more_container = games_in_a_day[-1].find_element(By.CLASS_NAME,"trn-gamereport-list__group-more")
        load_more_button = driver.find_element(By.TAG_NAME,"button")      
        update_page(driver,load_more_button)
    except Exception as e:
        print("All games generated")
        break

all_game_links = []
games_in_a_day = driver.find_elements(By.CLASS_NAME,"trn-gamereport-list__group")
for current_game_day in games_in_a_day:
    games_played = current_game_day.find_elements(By.CLASS_NAME,"trn-gamereport-list__group-entries")
    for current_games in games_played:
        all_game_links = all_game_links + get_links_for_a_day(driver,current_games)
        #all_game_links.append(get_lower_html_from_element(driver,current_games))
        #parse_game_information(get_lower_html_from_element(driver,current_games))

print(all_game_links)    
print("all game links found!")

for game_link in all_game_links:
    parse_match_information(driver,game_link)

print("parsed all games!")
driver.quit()

for cur in compare_list:
    cur[0].print_stats()
    cur[1].print_stats()

quit()


'''
Legacy way to update the games
'''
# while True:
#     games_in_a_day = driver.find_elements(By.CLASS_NAME,"trn-gamereport-list__group")
#     for current_game_day in games_in_a_day:
#         try:
#             games_played = current_game_day.find_elements(By.CLASS_NAME,"trn-gamereport-list__group-entries")
#             if games_played:
#                 for current_games in games_played:
#                     parse_game_information(get_lower_html_from_element(driver,current_games))
#             else:
#                 x = driver.find_element(By.TAG_NAME,"button")
#                 print(x)        
#                 update_page(driver,x)
#         except Exception:
#             break