import argparse
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
    def getPage(self, url: str, params: dict = {}):
        try:
            req = requests.get(url, params=params, headers=HEADERS)
            req.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve the webpage. Error: {e}", file=sys.stderr)
            return (None, None)

        return (BeautifulSoup(req.text, "html.parser"), req.url)

    def getLinks(self, url: str):
        bs = self.getPage(url)[0]

        if bs is not None:
            promoted_urls = []
            promoted_listings = bs.find(
                "div", {"data-cy": "search.listing.promoted"}
            ).find_all("a", {"data-cy": "listing-item-link"})
            for link in promoted_listings:
                if "href" in link.attrs:
                    promoted_urls.append(link.attrs["href"])

            organic_urls = []
            organic_listings = bs.find(
                "div", {"data-cy": "search.listing.organic"}
            ).find_all("a", {"data-cy": "listing-item-link"})
            for link in organic_listings:
                if "href" in link.attrs:
                    organic_urls.append(link.attrs["href"])

            return (promoted_urls, organic_urls)
        return None

    def getListing(self, pageUrl: str, promoted: bool):
        url = "http://www.otodom.pl{}".format(pageUrl)
        bs = self.getPage(url)[0]

        if bs is not None:
            listing = dict()
            listing["url"] = url

            try:
                id_match = re.search(
                    "[0-9]+$",
                    bs.find("meta", {"name": "description"}).get("content", ""),
                )
                listing["otodom_id"] = id_match.group() if id_match else ""

                listing["title"] = bs.find("h1", {"data-cy": "adPageAdTitle"}).text

                localization = dict()
                adres = bs.find("a", {"aria-label": "Adres"}).text.split(",")

                match len(adres):
                    case x if x >= 4:
                        localization["province"] = adres[-1].strip()
                        localization["city"] = adres[-2].strip()
                        localization["district"] = adres[1].strip()
                        localization["street"] = adres[0].strip()
                    case _:
                        localization["province"] = ""
                        localization["city"] = adres[-1].strip()
                        localization["district"] = ""
                        localization["street"] = adres[0].strip()

                listing["localization"] = localization

                listing["promoted_urls"] = promoted

                number = bs.find("strong", {"aria-label": "Cena"}).text.replace(
                    ",", "."
                )
                listing["price"] = int(float(re.sub(r"[^.0-9]", "", number)))

                number = bs.find(
                    "div", {"data-testid": "table-value-rooms_num"}
                ).text.replace(",", ".")
                listing["rooms"] = int(float(re.sub(r"[^.0-9]", "", number)))

                number = bs.find(
                    "div", {"data-testid": "table-value-area"}
                ).text.replace(",", ".")
                listing["area"] = int(float(re.sub(r"[^.0-9]", "", number)))

                listing["estate_agency"] = bs.find(
                    "div", {"data-testid": "table-value-advertiser_type"}
                ).text

                return listing

            except Exception:
                print("Listing URL:{url} is missing something", file=sys.stderr)

        return None

    def scrap_listings(self, url, params={}):
        bs, url = self.getPage(url, params=params)
        print(f"Base URL: {url}")

        if bs is not None:
            processed_urls = set()
            scraped_data = []

            number_of_pages = int(
                bs.find("nav", {"data-cy": "pagination"}).find_all("a")[-1].text
            )

            for page_number in range(1, number_of_pages + 1):
                print(f"Scraping page nr: {page_number}...")

                listing_links = self.getLinks(url + "&page={}".format(page_number))

                # promoted_urls ads
                for listing_url in listing_links[0]:
                    if listing_url not in processed_urls:
                        processed_urls.add(listing_url)
                        result = self.getListing(listing_url, promoted=True)
                        if result is not None:
                            scraped_data.append(result)

                # organic_urls ads
                for listing_url in listing_links[1]:
                    if listing_url not in processed_urls:
                        processed_urls.add(listing_url)
                        result = self.getListing(listing_url, promoted=False)
                        if result is not None:
                            scraped_data.append(result)

            with open("otodom_listing.json", "w", encoding="utf-8") as json_file:
                json.dump(scraped_data, json_file, ensure_ascii=False, indent=2)

    def generate_url(self):
        with open("otodom_settings.json") as f:
            data = json.load(f)

            url = data["base_url"] + "pl/wyniki"

            if data["only_for_sale"]:
                url += "/sprzedaz"
            elif data["only_for_rent"]:
                url += "/wynajem"
                url += "/" + data["property_type"] + "/"

            if len(data["province"]) > 0:
                url += data["province"] + "/" + data["city"] + "?"
            else:
                url += "cala-polska?"

            params = {
                "priceMin": data["price_min"],
                "priceMax": data["price_max"],
                "viewType": "listing",
                "by": "LATEST",
                "direction": "DESC",
                "limit": "72",
            }

            return (url, params)


if __name__ == "__main__":
    crawler = Crawler()

    parser = argparse.ArgumentParser(description="Otodom Listing Scrapper")
    parser.add_argument(
        "-u", "--url", help="Specify the base URL for scraping listings"
    )
    parser.add_argument(
        "-s",
        "--settings",
        nargs="?",
        const=True,
        help="Generate base URL from otodom_setting.json",
    )
    args = parser.parse_args()

    if args.url:
        crawler.scrap_listings(args.url)
    elif args.settings:
        print("URL generated from otodom_settings.json")
        crawler.scrap_listings(*crawler.generate_url())
    else:
        url = input("Enter URL: ")
        crawler.scrap_listings(url)
