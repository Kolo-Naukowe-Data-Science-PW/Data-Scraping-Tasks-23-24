import requests
from bs4 import BeautifulSoup, Tag
from HouseItem import HouseItem


class Scraper:
    TARGET_URL = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa?limit=72"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    def __init__(self):
        self.itemLinksVisited = []

    def startScraping(self, limit: int = 200) -> [HouseItem]:
        response = requests.get(self.TARGET_URL, headers=self.headers)
        if response.status_code // 100 != 2:
            print("ERROR: Could not load initial page")
            return []

        soup = BeautifulSoup(response.content, features="html.parser")
        lastPageElem = soup.select_one('nav[data-cy="pagination"] a:last-of-type')
        if lastPageElem is None:
            print("ERROR: no pagination found on the page")
            return []

        scrapedPages = []
        maxPage = int(lastPageElem.getText())
        for page in range(0, maxPage):
            print(f"> Start scraping page {page+1}...")
            scrapedPages = scrapedPages + self.getPage(page + 1)
            print(f"> Scraped {len(scrapedPages)} objects")
            if len(scrapedPages) >= limit:
                break
        return scrapedPages

    def getPage(self, page: int = 1) -> [HouseItem]:
        response = requests.get(f"{self.TARGET_URL}&page={page}", headers=self.headers)
        if response.status_code // 100 != 2:
            print(f"ERROR: could not load new page, status: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, features="html.parser")
        linkElems = soup.select('a[href^="/pl/oferta/"]')
        links = [elem.get("href") for elem in linkElems]

        linksFiltered = list(filter(self.filterRepeatedLinks, links))
        self.itemLinksVisited.extend(linksFiltered)
        return list(map(self.mapHouseItemLinks, linksFiltered))

    def filterRepeatedLinks(self, suburl: str):
        return suburl not in self.itemLinksVisited

    def mapHouseItemLinks(self, suburl: str):
        return self.scrapHouseItem(f"{HouseItem.base_url}{suburl}")

    def scrapHouseItem(self, url: str):
        response = requests.get(url, headers=self.headers)
        if response.status_code // 100 != 2:
            print(f"ERROR: could not load item page, status: {response.status_code}")

        soup = BeautifulSoup(response.content, features="html.parser")
        titleElem = soup.select_one('h1[data-cy="adPageAdTitle"]')
        title = titleElem.getText() if titleElem is not None else ""
        priceElem = soup.select_one('[data-cy="adPageHeaderPrice"]')
        price = priceElem.getText() if priceElem is not None else ""
        areaElem = soup.select_one(
            '[aria-label="Powierzchnia"] [data-testid="table-value-area"]'
        )
        area = areaElem.getText() if areaElem is not None else ""
        roomsElem = soup.select_one('[aria-label="Liczba pokoi"] a')
        rooms = roomsElem.getText() if roomsElem is not None else ""
        localElem = soup.select_one('a[href="#map"][aria-label="Adres"]')
        localization = localElem.getText() if localElem is not None else ""
        agencyElem = soup.select_one(
            '[aria-label="Typ ogłoszeniodawcy"] [data-testid="table-value-advertiser_type"]'
        )
        agency = agencyElem.getText() if agencyElem is not None else ""

        item = HouseItem(url).setPrice(price).setTitle(title).setArea(area)
        item.setLocalization(localization).setRooms(rooms).setEstateAgency(agency)
        return item
