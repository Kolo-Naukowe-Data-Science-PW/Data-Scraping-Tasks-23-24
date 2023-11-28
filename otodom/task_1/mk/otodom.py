import json
import re
import sys

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "text/html; charset=utf-8",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
    "Sec-Ch-Ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",  # noqa: E501
}


class Crawler:
    def getPage(self, url):
        try:
            req = requests.get(url, headers=HEADERS)
        except requests.exceptions.RequestException:
            print(f"Failed to retrieve the webpage. Status code: {req.status_code}")
            return None
        return BeautifulSoup(req.text, "html.parser")

    def getLinks(self, url):
        bs = self.getPage(url)
        if bs is not None:
            promoted_listings = bs.find(
                "div", {"data-cy": "search.listing.promoted"}
            ).find_all("a", {"class": "css-1hfdwlm e1dfeild2"})
            promoted = []
            for link in promoted_listings:
                if "href" in link.attrs:
                    promoted.append(link.attrs["href"])

            organic_listings = bs.find(
                "div", {"data-cy": "search.listing.organic"}
            ).find_all("a", {"class": "css-1hfdwlm e1dfeild2"})
            organic = []
            for link in organic_listings:
                if "href" in link.attrs:
                    organic.append(link.attrs["href"])

            return (promoted, organic)
        return None

    def getListing(self, pageUrl, promoted):
        url = "http://www.otodom.pl{}".format(pageUrl)
        bs = self.getPage(url)
        if bs is not None:
            listing = dict()
            listing["url"] = url

            id_match = re.search(
                "[0-9]+$", bs.find("meta", {"name": "description"}).get("content", "")
            )
            listing["otodom_id"] = id_match.group() if id_match else ""

            listing["title"] = bs.find("h1", {"class": "css-1wnihf5 efcnut38"}).text

            localization = dict()
            l10n = bs.find("a", {"class": "e1w8sadu0 css-1helwne exgq9l20"}).text.split(
                ","
            )

            localization["province"] = l10n[-1] if len(l10n) >= 4 else ""
            localization["city"] = l10n[-2] if len(l10n) >= 4 else l10n[-1]
            localization["district"] = l10n[1] if len(l10n) >= 4 else ""
            localization["street"] = l10n[0] if len(l10n) >= 4 else l10n[0]

            listing["localization"] = localization

            listing["promoted"] = promoted
            number = bs.find("strong", {"class": "css-t3wmkv e1l1avn10"}).text.replace(
                ",", "."
            )
            listing["price"] = int(float(re.sub(r"[^.0-9]", "", number)))
            number = bs.find(
                "div", {"data-testid": "table-value-rooms_num"}
            ).text.replace(",", ".")
            listing["rooms"] = int(float(re.sub(r"[^.0-9]", "", number)))
            number = bs.find("div", {"data-testid": "table-value-area"}).text.replace(
                ",", "."
            )
            listing["area"] = int(float(re.sub(r"[^.0-9]", "", number)))
            listing["estate_agency"] = bs.find(
                "div", {"data-testid": "table-value-advertiser_type"}
            ).text

            return listing
        return None

    def scrap_listings(self, url, check_all_pages=False):
        bs = self.getPage(url)

        if bs is not None:
            listings_url = set()
            listing_json = []

            number_of_pages = 1
            if check_all_pages:
                page_numeration = bs.find_all(
                    "a", {"class": "eo9qioj1 css-5tvc2l edo3iif1"}
                )
                number_of_pages = max([int(num.text) for num in page_numeration])

            for page_number in range(1, number_of_pages + 1):
                print(page_number)
                listing_links = self.getLinks(url + "?page={}".format(page_number))
                # listing_links = self.getLinks(url)
                # promoted ads
                for listing_url in listing_links[0]:
                    if listing_url not in listings_url:
                        listings_url.add(listing_url)
                        listing_json.append(self.getListing(listing_url, promoted=True))

                # organic ads
                for listing_url in listing_links[1]:
                    if listing_url not in listings_url:
                        listings_url.add(listing_url)
                        listing_json.append(
                            self.getListing(listing_url, promoted=False)
                        )

            with open("otodom_listing.json", "w", encoding="utf-8") as json_file:
                json.dump(listing_json, json_file, ensure_ascii=False, indent=2)

    def generate_url(self):
        with open("otodom_settings.json") as f:
            data = json.load(f)
            url = data["base_url"] + "pl/wyniki"

            if data["only_for_sale"]:
                url += "/sprzedaz"

            if data["only_for_rent"]:
                url += "/wynajem"
                url += "/" + data["property_type"] + "/"
            if len(data["province"]) > 0:
                url += data["province"] + "/" + data["city"] + "?"
            else:
                url += "cala-polska?"

            url += "limit=36"

            if len(data["price_min"]) > 0:
                url += "&priceMin=" + data["price_min"]

            if len(data["price_max"]) > 0:
                url += "&priceMax=" + data["price_max"]

            url += "&by=LATEST&direction=DESC&viewType=listing"
            # print("Generated link:\n", url)
            return url


if __name__ == "__main__":
    crawler = Crawler()

    if len(sys.argv) > 2 and sys.argv[1] == "-u":
        print(sys.argv[2])
        crawler.scrap_listings(sys.argv[2], check_all_pages=False)
    else:
        crawler.scrap_listings(crawler.generate_url(), check_all_pages=False)
