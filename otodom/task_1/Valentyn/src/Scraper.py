import requests
from bs4 import BeautifulSoup
from HouseItem import HouseItem


class Scraper:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    def __init__(self, url):
        self.TARGET_URL = url
        self.item_links_visited = []

    def start_scraping(self, limit: int = 200) -> [HouseItem]:
        response = requests.get(self.TARGET_URL, headers=self.headers)
        if response.status_code // 100 != 2:
            print("ERROR: Could not load initial page")
            return []

        soup = BeautifulSoup(response.content, features="html.parser")
        last_page_elem = soup.select_one('nav[data-cy="pagination"] a:last-of-type')
        if last_page_elem is None:
            print("ERROR: no pagination found on the page")
            print("Trying to scrape 1st (the only) page...")
            return self.get_page(1)

        scraped_pages = []
        max_page = int(last_page_elem.getText())
        for page in range(0, max_page):
            print(f"> Start scraping page {page+1}...")
            scraped_pages = scraped_pages + self.get_page(page + 1)
            print(f"> Scraped {len(scraped_pages)} objects")
            if len(scraped_pages) >= limit:
                break
        return scraped_pages

    def get_page(self, page: int = 1) -> [HouseItem]:
        response = requests.get(f"{self.TARGET_URL}&page={page}", headers=self.headers)
        if response.status_code // 100 != 2:
            print(f"ERROR: couldnt load new page, status: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, features="html.parser")
        link_elems = soup.select('a[href^="/pl/oferta/"]')
        links = [elem.get("href") for elem in link_elems]

        links_filtered = list(filter(self.filter_repeated_links, links))
        self.item_links_visited.extend(links_filtered)
        return list(map(self.map_house_item_links, links_filtered))

    def filter_repeated_links(self, suburl: str):
        return suburl not in self.item_links_visited

    def map_house_item_links(self, suburl: str):
        return self.scrap_house_item(f"{HouseItem.base_url}{suburl}")

    def scrap_house_item(self, url: str):
        response = requests.get(url, headers=self.headers)
        if response.status_code // 100 != 2:
            print(f"ERROR: didnt load item page, status: {response.status_code}")

        soup = BeautifulSoup(response.content, features="html.parser")
        title_elem = soup.select_one('h1[data-cy="adPageAdTitle"]')
        title = title_elem.getText() if title_elem else ""
        price_elem = soup.select_one('[data-cy="adPageHeaderPrice"]')
        price = price_elem.getText() if price_elem else ""
        area_elem = soup.select_one(
            '[aria-label="Powierzchnia"] [data-testid="table-value-area"]'
        )
        area = area_elem.getText() if area_elem else ""
        rooms_elem = soup.select_one('[aria-label="Liczba pokoi"] a')
        rooms = rooms_elem.getText() if rooms_elem else ""
        local_elem = soup.select_one('a[href="#map"][aria-label="Adres"]')
        localization = local_elem.getText() if local_elem else ""
        agency_elem = soup.select_one(
            """[aria-label="Typ ogłoszeniodawcy"]
             [data-testid="table-value-advertiser_type"]"""
        )
        agency = agency_elem.getText() if agency_elem else ""

        item = HouseItem(url).set_price(price).set_title(title).set_area(area)
        item.set_localization(localization).set_rooms(rooms)
        return item.set_estate_agency(agency)
