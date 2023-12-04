class HouseItem:
    base_url = "https://www.otodom.pl"

    def __init__(self, url: str):
        self.dictionary = {
            "url": url,
            "otodom_id": url[len(self.base_url) + 1 :],
            "price": None,
            "title": "",
            "rooms": None,
            "area": None,
            "estate_agency": "",
            "promoted": False,
            "localization": {
                "province": "",
                "city": "",
                "district": "",
                "street": "",
            },
        }

    def setPrice(self, priceStr: str):
        clean_price = priceStr.strip().replace(" zł", "").replace(" ", "")
        try:
            converted_price = int(clean_price)
            self.dictionary["price"] = converted_price
        except ValueError:
            self.dictionary["price"] = None
        finally:
            return self

    def setTitle(self, title: str):
        self.dictionary["title"] = title
        return self

    def setArea(self, area: str):
        cleanNumber = area.strip().split(" ")[0].replace(",", ".")
        self.dictionary["area"] = int(float(cleanNumber)) if cleanNumber != "" else None
        return self

    def setRooms(self, rooms: str):
        self.dictionary["rooms"] = int(rooms) if (rooms.strip() != "") else None
        return self

    def setLocalization(self, address: str):
        addressList = address.split(", ")
        if len(addressList) >= 5:
            self.dictionary["localization"]["street"] = addressList[-5]
        if len(addressList) >= 4:
            self.dictionary["localization"]["district"] = addressList[-3]
        if len(addressList) >= 3:
            self.dictionary["localization"]["city"] = addressList[-2]
        if len(addressList) >= 1:
            self.dictionary["localization"]["province"] = addressList[-1]
        return self

    def setEstateAgency(self, agency: str):
        self.dictionary["estate_agency"] = agency
        return self

    def toDictionary(self):
        return self.dictionary
