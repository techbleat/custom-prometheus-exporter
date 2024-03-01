import requests
import time
import random

from bs4 import BeautifulSoup

from prometheus_client import start_http_server
from prometheus_client.core import  GaugeMetricFamily, REGISTRY


# we are only interested in these labels; club,player name and photo
# we are only intereste in thess data; goals_scored, assists, games played and total game time

class CustomCollector(object):
    team_data_link = {}
    players_img= {}
    
    def __init__(self):
        url = "https://fbref.com/en/comps/9/Premier-League-Stats"
        headers = {'User-Agent': 'Mozilla/5.0'}
        info = requests.get(url,headers=headers).text

        # Parsing Premier League data
        soup = BeautifulSoup(info, "html.parser")
        #print (soup)
        
        table = soup.find("table", id="results2023-202491_overall")
        table_body = table.find("tbody")
        rows = table_body.find_all("tr")
        
        # extract all the clubs url locations
        for row in rows:
            line = str(row)
            href_line = line[line.find("href=") :]
            team_url = (
                "https://fbref.com"
                + href_line[href_line.find("/") : href_line.find('">')]
            )
            team_name = href_line[href_line.find('">') : href_line.find("</a")][2:]
            self.team_data_link[team_name] = team_url
            
            #print (team_name, team_url)
            
    def _lazy_image_extract(self,link,player_name):
        
        players_to_fetch_image = ["Bukayo Saka","Declan Rice", "William Saliba", "Ben White","Aaron Ramsdale"]
        if player_name in players_to_fetch_image:

           url = "https://fbref.com" + link
           headers = {'User-Agent': 'Mozilla/5.0'}
           info = requests.get(url,headers=headers).text
           soup = BeautifulSoup(info, "html.parser")
           div = soup.find("div", id="info")
           img = div.find("img")
           self.players_img [player_name] = img['src'] 
        else:
            self.players_img [player_name] = "https://cdn.britannica.com/68/195168-050-BBAE019A/football.jpg"
        return self.players_img [player_name]
            
        
    def collect(self):
        
        #for club in self.team_data_link.keys():    
        #we wont use this, as the target website restricts us to only a few crawls 
        
        club_subset = ['Arsenal']  # a subset of self.team_data_link dictionary
        
        for club in club_subset:
            
            time.sleep(3)  #gentle crawl so we don't get banned/penalised  
            info = requests.get(self.team_data_link[club]).text
            soup = BeautifulSoup(info, "html.parser")
            table = soup.find("table", id="stats_standard_9")  
            table_body = table.find("tbody")

            rows = table_body.find_all("tr")
            img_extract_count = 0
            for row in rows:
                players_stat = {}
                cells = row.find_all("td")        
                players_stat ["player"] = row.find("th").find('a').contents[0]
                players_stat ["starts"] = cells[3].text or 0
                players_stat ["minutes_played"] = cells[5].text.replace(',','') or 0
                players_stat ["goals_scored"] = cells[7].text or 0
                players_stat ["assists"] = cells[8].text or 0
                
                player_href = row.find("th").find('a').get('href') 
                
                player_photo = ""
                if not (players_stat ["player"] in self.players_img.keys()):
                    if img_extract_count < 4:   #gentle crawl so we don't get banned/penalised  
                      player_photo = self._lazy_image_extract (player_href,players_stat ["player"] )
                      img_extract_count = img_extract_count + 1
                else:
                    player_photo = self.players_img [players_stat ["player"]] 
                
                player_name = ""
                for data_key in players_stat.keys():
                    if  data_key == "player":
                            player_name = players_stat ["player"] 
                    else :
                            gauge = GaugeMetricFamily(data_key, '', labels=['club','player','image'])
                            gauge.add_metric([club,player_name,player_photo], players_stat[data_key])
                            yield gauge
                            
        
        for row in rows:
            line = str(row)
            href_line = line[line.find("href=") :]
            team_url = (
                "https://fbref.com"
                + href_line[href_line.find("/") : href_line.find('">')]
            )
            team_name = href_line[href_line.find('">') : href_line.find("</a")][2:]
            self.team_data_link[team_name] = team_url
        
    

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    print ("Starting export process ..") 
    REGISTRY.register(CustomCollector())
    start_http_server(8000)
    print ("successfully started ")
    while True:
        time.sleep(random.randrange(1,10))
