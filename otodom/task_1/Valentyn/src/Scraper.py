import requests
from bs4 import BeautifulSoup, Tag
from HouseItem import HouseItem


class Scraper:
    TARGET_URL = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa?limit=32"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    def getPage(self, page: int = 1) -> [HouseItem]:
        response = requests.get(f"{self.TARGET_URL}&page={page}", headers=self.headers)
        print(response.status_code)
        if response.status_code // 100 != 2:
            print("ERROR: some error happened")
            return

        soup = BeautifulSoup(response.content, features="html.parser")
        links = soup.select('a[href^="/pl/oferta/"]')

        return list(map(self.mapHouseItemLinks, links))

    def mapHouseItemLinks(self, link_item: Tag):
        suburl = link_item.get("href", "")
        return self.scrapHouseItem(f"{HouseItem.base_url}{suburl}")

    def scrapHouseItem(self, url: str):
        response = requests.get(url, headers=self.headers)
        if response.status_code // 100 != 2:
            print("ERROR: some error happened")

        soup = BeautifulSoup(response.content, features="html.parser")
        title = soup.select_one('h1[data-cy="adPageAdTitle"]').getText()
        price = soup.select_one('[data-cy="adPageHeaderPrice"]').getText()

        item = HouseItem(url).setPrice(price).setTitle(title)
        return item
