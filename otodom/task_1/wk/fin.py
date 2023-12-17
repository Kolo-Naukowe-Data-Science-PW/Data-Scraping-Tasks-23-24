import json
import random
import re
import sys
import time

import requests
from bs4 import BeautifulSoup
from generate_link import generate_link

HEADERS = {
    "User-Agent": """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"""
}


def scrape_single_record(record):
    record_dict = {}

    record_dict["title"] = record.find(
        "span",
        {"data-cy": "listing-item-title"}
    ).string

    loc = ""
    tag = record.find_all("p", {"title": True})[0]
    if tag.has_attr("title"):
        loc = {}
        info = tag.string.split(", ")
        loc["province"] = info[-1]
        loc["city"] = info[-2]
        if info[0].startswith("ul.") or info[0].startswith("al."):
            loc["district"] = ", ".join(info[1:-2])
            loc["street"] = info[0]
        else:
            loc["district"] = ", ".join(info[0:-2])
            loc["street"] = ""

    record_dict["localization"] = loc

    record_dict["promoted"] = False
    span_tags = record.find_all("span")
    for span_tag in span_tags:
        if len(span_tag.find_all("p")) == 1:
            record_dict["promoted"] = True

    regex = re.compile("zł")
    zl = record.find_all(string=regex, title=None)
    if len(zl) > 0:
        record_dict["price"] = (zl[0].string).replace("\xa0", " ")
    else:
        record_dict["price"] = ""

    regex = re.compile("^[0-9].*pok")
    record_dict["rooms"] = int(
        re.findall("[0-9]+",
                   record.find("span", title=None, string=regex).string)[0]
    )

    regex = re.compile(".*[^zł/]m²")
    record_dict["area"] = int(
        float(
            record.find("span", title=None, string=regex)
            .string[:-3]
            .replace("\xa0", "")
            .replace(",", ".")
        )
    )

    estate_agency = record.find_all("span",
                                    {"data-testid": "listing-item-owner-name"})
    record_dict["estate_agency"] = (
        estate_agency[0].string if len(estate_agency) > 0 else ""
    )

    return record_dict


if __name__ == "__main__":
    url, params = generate_link()
    response = requests.get(url, headers=HEADERS, params=params)
    doc = BeautifulSoup(response.text, "html.parser")

    # let"s check how many pages we have to scrap data from
    regex = re.compile("[0-9]+")
    result = doc.find_all("nav", {"data-cy": "pagination"})
    result = result[-1].find_all("a")[-1]["data-cy"]
    pages_n = int(re.findall(regex, result)[0])

    scrapped_data = []
    for i in range(1, pages_n+1):
        url = url + "?page=" + str(i)
        response = requests.get(url, headers=HEADERS)
        if str(response.status_code)[0] == '4':
            with open("db.json", "w", encoding="utf-8") as file:
                json.dump(scrapped_data, file, ensure_ascii=False, indent=4)
            print("Already scrapped data saved in db.json")
            print("Client error" + str(response.status_code) +
                  "occured on page " + str(i) + ". Aborting.")
            sys.exit(1)
        else:
            print(f"Scrapping {i}/{pages_n} page...")

            doc = BeautifulSoup(response.text, "html.parser")
            records = doc.select("article")
            listings_ids = doc.find_all("a", {"data-cy": "listing-item-link"})
            assert len(records) == len(listings_ids)

            for i in range(0, len(records)):
                record_dict = {
                    "url":
                        "https://www.otodom.pl" + listings_ids[i]["href"],
                    "otodom_id":
                        re.findall("ID(.*)", listings_ids[i]["href"])[0],
                }
                record_dict.update(scrape_single_record(records[i]))
                scrapped_data.append(record_dict)

        time.sleep(random.uniform(0.2, 0.5))

    print("Scrapping completed : ~ D")
    with open("db.json", "w", encoding="utf-8") as file:
        json.dump(scrapped_data, file, ensure_ascii=False, indent=4)
        file.write("\n")

    print("Scapped data saved in db.json")
