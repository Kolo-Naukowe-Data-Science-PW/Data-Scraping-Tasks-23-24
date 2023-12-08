import unicodedata


class HouseItem:
    base_url = "https://www.otodom.pl"

    def __init__(self, url: str):
        self.dictionary = {
            "url": url,
            "otodom_id": url[slice(len(self.base_url) + 1, None)],
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
        normalized = unicodedata.normalize("NFKD", text.replace("ł", "l"))
        ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
        return ascii_text

    def set_price(self, price_str: str):
        clean_price = price_str.strip().replace(" zł", "").replace(" ", "")
        try:
            converted_price = int(clean_price)
            self.dictionary["price"] = converted_price
        except ValueError:
            self.dictionary["price"] = None
        finally:
            return self

    def set_title(self, title: str):
        self.dictionary["title"] = self.convert_to_ascii(title)
        return self

    def set_area(self, area: str):
        clean_number = area.strip().split(" ")[0]
        clean_number = clean_number.replace(",", ".").replace("\xa0", "")
        self.dictionary["area"] = (
            int(float(clean_number)) if clean_number != "" else None
        )
        return self

    def set_rooms(self, rooms: str):
        self.dictionary["rooms"] = None
        if rooms.strip() != "":
            self.dictionary["rooms"] = int(rooms)
        return self

    def set_localization(self, address: str):
        address_list = address.split(", ")
        if len(address_list) >= 5:
            street = self.convert_to_ascii(address_list[-5])
            self.dictionary["localization"]["street"] = street
        if len(address_list) >= 4:
            district = self.convert_to_ascii(address_list[-3])
            self.dictionary["localization"]["district"] = district
        if len(address_list) >= 3:
            city = self.convert_to_ascii(address_list[-2])
            self.dictionary["localization"]["city"] = city
        if len(address_list) >= 1:
            province = self.convert_to_ascii(address_list[-1])
            self.dictionary["localization"]["province"] = province
        return self

    def set_estate_agency(self, agency: str):
        self.dictionary["estate_agency"] = self.convert_to_ascii(agency)
        return self

    def to_dictionary(self):
        return self.dictionary
