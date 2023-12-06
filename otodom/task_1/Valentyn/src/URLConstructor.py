import urllib.parse
import json


class URLConstructor:
    def from_json(pathfile: str = "settings.json"):
        with open(pathfile, "r") as json_file:
            settings = json.load(json_file)

            query_params = {"limit": 72}
            if settings["price_min"]:
                query_params["priceMin"] = settings["price_min"]
            if settings["price_max"]:
                query_params["priceMax"] = settings["price_max"]

            url = settings["base_url"]
            if settings["sale_or_rent"] == "sale":
                url = url + "sprzedaz/"
            else:
                url = url + "wynajem/"

            property_type = settings["property_type"]
            province = settings["province"].replace("-", "--")
            city = settings["city"]
            url = url + f"{property_type}/{province}/{city}/{city}/{city}"
            query_params_string = urllib.parse.urlencode(query_params)
            final_url = url + "?" + query_params_string
            print(final_url)
            return final_url
