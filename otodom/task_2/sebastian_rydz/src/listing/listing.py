import json

from bs4 import ResultSet
from settings.s_types import Defaults


class Listing:
    """
    A class that represents a listing on the otodom.pl website.
    """

    def __init__(self, code: ResultSet):
        self.link = Defaults.DEFAULT_URL + self.extract_link(code)
        self.promoted = self.extract_promoted(code)
        self.province = ""
        self.city = ""
        self.district = ""
        self.street = ""
        self.otodom_id = ""
        self.title = ""
        self.price = 0
        self.price_for_m2 = 0
        self.offered_by = ""
        self.estate_agency_name = ""
        self.estate_agency_street = ""
        self.estate_agency_city = ""
        self.estate_agency_postal_code = ""
        self.estate_agency_county = ""
        self.estate_agency_province = ""

    def __repr__(self) -> dict:
        return self.__dict__.__repr__()

    @staticmethod
    def extract_link(code: ResultSet) -> str:
        """
        Extracts the link from the HTML code.

        :param code: The HTML code containing the link
        :return: The extracted link
        """
        return code.select_one("a")["href"]

    @staticmethod
    def extract_promoted(code: ResultSet) -> bool:
        """
        Determines whether the listing is promoted.

        :param code: The HTML code containing the promotion status
        :return: True if the listing is promoted, False otherwise
        """
        return code.select_one("article>span+div") is not None

    @staticmethod
    def extract_localization(properties: dict) -> (str, str, str, str):
        """
        Extracts the localization details from the properties.

        :param properties: The properties containing the localization details
        :return: A tuple containing the province, city, district, and street
        """
        province = properties["ad"]["location"]["address"]["province"]["code"]
        city = properties["ad"]["location"]["address"]["city"]["code"]
        district = properties["ad"]["location"]["address"].get("district", "")
        if isinstance(district, dict):
            district = district["name"]
        street = properties["ad"]["location"]["address"].get("street", "")
        if isinstance(street, dict):
            street = street["name"]
        return province, city, district, street

    @staticmethod
    def extract_offered_by(properties: dict) -> str:
        """
        Determines the offer type from the properties.

        :param properties: The properties containing the offer type
        :return: The offer type
        """
        return "private" if properties["ad"]["agency"] is None else "estate_agency"

    @staticmethod
    def extract_estate_agency_name(properties: dict) -> str:
        """
        Extracts the name of the estate agency from the properties.

        :param properties: The properties containing the estate agency name
        :return: The name of the estate agency
        """
        return properties["ad"]["agency"]["name"]

    @staticmethod
    def extract_estate_agency_details(properties: dict) -> str:
        """
        Extracts the details of the estate agency from the properties.

        :param properties: The properties containing the estate agency details
        :return: The details of the estate agency
        """
        address = properties["ad"]["agency"]["address"].strip().split(", ")
        if len(address) > 5:
            address = address[2:]
        return address[0], address[1], address[2], "".join(address[3:-1]), address[-1]

    def extract_data_from_page(self, code: ResultSet) -> None:
        """
        Extracts data from the page and updates the Listing instance.

        This method loads the listing information from a script tag in the HTML code,
        parses it as JSON, and uses it to update the attributes of the Listing instance.

        :param code: The HTML code containing the listing information
        """
        listing_information = json.loads(
            code.find("script", {"type": "application/json"}).text
        )
        listing_properties = listing_information["props"]["pageProps"]
        self.otodom_id = listing_properties["ad"]["id"]
        self.title = listing_properties["ad"]["title"]
        (
            self.province,
            self.city,
            self.district,
            self.street,
        ) = self.extract_localization(listing_properties)
        self.price = listing_properties["ad"]["target"].get("Price", 0)
        self.price_for_m2 = listing_properties["ad"]["target"].get("Price_per_m", 0)
        self.offered_by = self.extract_offered_by(listing_properties)
        if self.offered_by == "estate_agency":
            (
                self.estate_agency_street,
                self.estate_agency_postal_code,
                self.estate_agency_city,
                self.estate_agency_county,
                self.estate_agency_province,
            ) = self.extract_estate_agency_details(listing_properties)
