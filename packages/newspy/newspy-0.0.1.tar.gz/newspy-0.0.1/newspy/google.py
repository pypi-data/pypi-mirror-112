from urllib.parse import quote
from newsfetch.utils import BeautifulSoup, UserAgent
import requests

class google_search:

    def __init__(self, keyword, newspaper_url):

        self.keyword = keyword
        self.newspaper_url = newspaper_url

        random_headers = {'User-Agent': UserAgent().random,
                          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

        self.search_term = '"{}" site:{}'.format(self.keyword, self.newspaper_url)

        url = "https://www.google.com/search?q={}".format('+'.join(self.search_term.split()))
        
        url_list = []

        query = quote(url)
        r = requests.get(f"https://www.google.com/search?q={query}&rlz=1C1ONGR_enCA933CA933&oq={query}&aqs=chrome.0.69i59j69i64.342j0j9&sourceid=chrome&ie=UTF-8", headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}) 
        soup = BeautifulSoup(r.content, "lxml")
        for selector in [("a", "FLP8od"), ("div", "Z0LcW"), ("h2", "qrShPb"), ("span", "ILfuVd"), ("div", "wDYxhc"), ("span", "hgKElc")]:
            element = soup.find(selector[0], {"class": selector[1]})
            if element:
                return element.text

        flight = soup.find("a", {"class": "t0uMIc"})
        if flight:
            flight = flight[0]
            place = flight.find("div", {"class": "sy5fm"}).text
            price = flight.find("span", {"class": "AFyU"}).text
            stops, time = flight.find("div", {"class": "LIqvqf"}).findChildren("span")
            s = f"A flight to {place} with {stops} that lasts {time} costs {price}."
            return s
        
        results = soup.select("div.g")
        self.urls = [res.findChildren("div", {"class": "yuRUbf"})[0].findChildren("a")[0].get("href") for res in results]
