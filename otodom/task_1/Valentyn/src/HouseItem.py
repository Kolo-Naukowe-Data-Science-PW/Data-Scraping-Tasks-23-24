import json


class HouseItem:
    base_url = "https://www.otodom.pl"

    def __init__(self, url: str):
        self.url = url
        self.otodom_id = url[len(self.base_url) + 1 :]
        self.price = ""
        self.title = ""
        self.rooms = ""
        self.area = ""
        self.estate_agency = ""
        self.promoted = False
        self.localization = {
            "province": "",
            "city": "",
            "district": "",
            "street": "",
        }

    def setPrice(self, priceStr: str):
        self.price = priceStr
        return self

    def setTitle(self, title: str):
        self.title = title
        return self

    def toDictionary(self):
        return {
            "url": self.url,
            "otodom_i": self.otodom_id,
            "price": self.price,
            "title": self.title,
            "rooms": self.rooms,
            "area": self.area,
            "estate_agency": self.estate_agency,
            "promoted": self.promoted,
            "localization": self.localization,
        }
