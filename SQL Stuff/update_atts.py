import time
import sqlite3
import csv
import scrapy
from scrapy.crawler import CrawlerProcess

# establish connection
conn = sqlite3.connect("player_stats.db")
cursor = conn.cursor()

# method to get all batter urls
def get_bat_urls():
    
    # init blank url list
    urls = []

    # query all ids
    cursor.execute("SELECT player_id FROM bat_atts;")
    id_rows = cursor.fetchall()

    # create urls and add them to the list
    for row in id_rows:
        (pid, ) = row
        url = f"https://www.baseball-reference.com/players/{pid[0]}/{pid}.shtml"
        urls.append(url)

    # return all urls
    return urls

# method to get all pitcher urls
def get_pit_urls():

    # init blank url list
    urls = []

    # query all ids
    cursor.execute("SELECT player_id FROM pit_atts;")
    id_rows = cursor.fetchall()

    # create urls and add them to the list
    for row in id_rows:
        (pid, ) = row
        url = f"https://www.baseball-reference.com/players/{pid[0]}/{pid}.shtml"
        urls.append(url)

    # return all urls
    return urls

class MySpider(scrapy.Spider):

    name = "my_spider"

    # assign urls
    # bat_urls = ["https://www.baseball-reference.com/players/d/deverra01.shtml"]
    # pit_urls = ["https://www.baseball-reference.com/players/s/skenepa01.shtml"]
    bat_urls = get_bat_urls()
    pit_urls = get_pit_urls()

    async def start(self):
        # parse through batters
        for url in self.bat_urls:
            time.sleep(1)
            yield scrapy.Request(url, callback=self.bat_parse)

        # parse through pitchers
        for url in self.pit_urls:
            time.sleep(1)
            yield scrapy.Request(url, callback=self.pit_parse)
    
    # method for parsing batter stat pages
    def bat_parse(self, response):
        # batters require BB%, AVG, HR, and H
        time.sleep(1)
        pid = response.url.split("/")[-1].split(".")[0]

        # get H, HR, AVG
        std_row = response.xpath(".//tr[@id='players_standard_batting.2025'][1]")
        hits = int(std_row.xpath("./td[@data-stat='b_h']//text()").extract_first())
        hrs = int(std_row.xpath("./td[@data-stat='b_hr']//text()").extract_first())
        avg = float(std_row.xpath("./td[@data-stat='b_batting_avg']//text()").extract_first())

        # get BB%
        adv_row = response.xpath(".//tr[@id='players_advanced_batting.2025'][1]")
        bbperc = float(adv_row.xpath("./td[@data-stat='b_base_on_balls_perc']//text()").extract_first()) / 100

        # add data for csv file
        bat_data.append([pid, hits, hrs, avg, bbperc])

        # calculate attributes
        con = round((avg + 0.035)/0.004)
        pow = round(((hrs/hits) + 0.5573)/0.01)
        eye = round((bbperc + 0.2407)/0.00464)

        # update player attributes to these values
        comm = f"""UPDATE bat_atts
        SET con = {con}, pow = {pow}, eye = {eye}
        WHERE player_id = '{pid}';"""

        cursor.execute(comm)

    # method for parsing pitcher stat pages
    def pit_parse(self, response):
        # pitchers require BB%, BAA, TBF, H, BB, K, and GB%
        time.sleep(1)
        pid = response.url.split("/")[-1].split(".")[0]

        # get BB, K, TBF
        std_row = response.xpath(".//tr[@id='players_standard_pitching.2025'][1]")
        hits = int(std_row.xpath("./td[@data-stat='p_h']//text()").extract_first())
        walks = int(std_row.xpath("./td[@data-stat='p_bb']//text()").extract_first())
        ks = int(std_row.xpath("./td[@data-stat='p_so']//text()").extract_first())
        tbf = int(std_row.xpath("./td[@data-stat='p_bfp']//text()").extract_first())

        # get BAA, BB%, GB%
        adv_row = response.xpath(".//tr[@id='players_advanced_pitching.2025'][1]")
        baa = float(adv_row.xpath("./td[@data-stat='p_batting_avg']//text()").extract_first())
        bbperc = float(adv_row.xpath("./td[@data-stat='p_base_on_balls_perc']//text()").extract_first()) / 100
        gbperc = float(adv_row.xpath("./td[@data-stat='p_gb_perc']//text()").extract_first()) / 100

        # add data for csv file
        pit_data.append([pid, bbperc, baa, tbf, hits, walks, ks, gbperc])

        # calculate attributes
        # for formulas, refer to Player module
        cmd = round((0.2262 - bbperc)/0.00203)
        vel = round(ks/(0.0095*(tbf - hits - walks)) + 36.18)
        stf = round((0.42 - baa)/0.0025)

        # update player attributes to these values
        comm = f"""UPDATE pit_atts
        SET cmd = {cmd}, vel = {vel}, stf = {stf}, gbrate = {gbperc}
        WHERE player_id = '{pid}';"""

        cursor.execute(comm)


# initialize header rows
bat_data = [["Player ID", "H", "HR", "AVG", "BB%"]]
pit_data = [["Player ID", "BB%", "BAA", "TBF", "H", "BB", "K", "GB%"]]

# get data
process = CrawlerProcess()
process.crawl(MySpider)
process.start()

# load raw data to csv files
with open("Web Scraping/batter_raw_stats.csv", "w", newline="") as bat_file:
    writer = csv.writer(bat_file)
    writer.writerows(bat_data)

with open("Web Scraping/pitcher_raw_stats.csv", "w", newline="") as pit_file:
    writer = csv.writer(pit_file)
    writer.writerows(pit_data)

conn.commit()
conn.close()