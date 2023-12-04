import unicodedata


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

    def convert_to_ascii(self, text):
        normalized = unicodedata.normalize("NFKD", text.replace('ł', 'l'))
        ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
        return ascii_text

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
        self.dictionary["title"] = self.convert_to_ascii(title)
        return self

    def setArea(self, area: str):
        cleanNumber = area.strip().split(" ")[0].replace(",", ".").replace("\xa0", "")
        self.dictionary["area"] = int(float(cleanNumber)) if cleanNumber != "" else None
        return self

    def setRooms(self, rooms: str):
        self.dictionary["rooms"] = int(rooms) if (rooms.strip() != "") else None
        return self

    def setLocalization(self, address: str):
        addressList = address.split(", ")
        if len(addressList) >= 5:
            street = self.convert_to_ascii(addressList[-5])
            self.dictionary["localization"]["street"] = street
        if len(addressList) >= 4:
            district = self.convert_to_ascii(addressList[-3])
            self.dictionary["localization"]["district"] = district
        if len(addressList) >= 3:
            city = self.convert_to_ascii(addressList[-2])
            self.dictionary["localization"]["city"] = city
        if len(addressList) >= 1:
            province = self.convert_to_ascii(addressList[-1])
            self.dictionary["localization"]["province"] = province
        return self

    def setEstateAgency(self, agency: str):
        self.dictionary["estate_agency"] = self.convert_to_ascii(agency)
        return self

    def toDictionary(self):
        return self.dictionary
