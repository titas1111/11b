from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep

class WebScraper:

    def __init__(self, page):
        self.page = page
        self.tmp = []
        self.ListOfScrapedFlatInfo = []
    def return_html(self):
        # html_file = open(self.page, "r", encoding="utf-8")
        html_file = requests.get(self.page)
        return_html = BeautifulSoup(html_file.text, "html.parser")
        return return_html

    def return_href(self):
        soup = self.return_html()
        self.tmp = [a["href"] for a in soup.find_all("a", href=True) if a.parent.name == 'h3']
        return [a["href"] for a in soup.find_all("a", href=True) if a.parent.name == 'h3']


class Aruodas(WebScraper):
    def loop(self):
    	
        for flat in self.tmp:
        	sleep(5)
        	self.ListOfScrapedFlatInfo.append((self.ScrapeFlat(flat)))

    def ScrapeFlat(self, page):
        d = {}
        self.page = page
        d["Adresas"] = self.page 
        soup = self.return_html()
        dd = soup.select("dd")
        dt = soup.select("dt")
        for i in range(20):
            try:
                tmp_val = str(dd[i].getText()).strip()
                tmp_name = str(dt[i].getText()).strip()
                d[tmp_name] = tmp_val
            except:
                return d
        return d


for i in range(45,55):
	aruodas = Aruodas("https://www.aruodas.lt/butu-nuoma/vilniuje/puslapis/"+str(i)+"/")
	aruodas.return_href() 
	aruodas.loop()

	output = pd.DataFrame()
	for d in aruodas.ListOfScrapedFlatInfo:
			output = output.append(d, ignore_index=True)
	output.to_excel("output "+str(i)+".xlsx", index=False)
	print(f"Done: {i}")