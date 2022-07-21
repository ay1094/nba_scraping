from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


threes = "https://www.nba.com/stats/teams/shots-closest-defender/?Season=2021-22&SeasonType=Regular%20Season&CloseDefDistRange=6%2B%20Feet%20-%20Wide%20Open&sort=FG3_PCT&dir=-1"
# threes4 = ""
# threes2 = "https://www.nba.com/stats/teams/shots-closest-defender/?Season=2021-22&SeasonType=Regular%20Season&sort=GP&dir=1&CloseDefDistRange=2-4%20Feet%20-%20Tight"
# threes0 = "https://www.nba.com/stats/teams/shots-closest-defender/?Season=2021-22&SeasonType=Regular%20Season&sort=GP&dir=1"


def getData(url_string, suffix_strings):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(threes)
    # src = driver.page_source
    # parser = BeautifulSoup(src, "lxml")
    select = Select(driver.find_element(By.NAME, "CloseDefDistRange"))
    for i in range(len(suffix_strings)):
        print("entering for loop")
        select.select_by_index(i)
        time.sleep(10)
        src = driver.page_source
        parser = BeautifulSoup(src, "lxml")
        print("i: " + str(i))
        table = parser.find("div", attrs={"class": "nba-stat-table__overflow"})
        headers_page = table.findAll("th")
        headers = [h.text.strip() for h in headers_page]
        headers = headers[4:]   #stripping the first header row hierarchial headers not necessary
        rows = table.findAll('tr')
        player_stats = [[td.getText().strip() for td in rows[i].findAll('td')] for i in range(len(rows))]
        stats = pd.DataFrame(player_stats, columns=headers)
        stats = stats[2:]
        stats.drop(['GP', 'G'], axis=1)
        stats = stats.add_suffix(suffix_strings[i])
        stats.rename(columns={"Team"+suffix_strings[i]: "Team"}, inplace=True)
        print(stats.head(5))
        filename = "nba_shooting"+suffix_strings[i]+".csv"
        stats.to_csv(filename, index=False)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    suffix_strings = ["_0-2", "_2-4", "_4-6", "_6+"]
    getData(threes, suffix_strings)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
