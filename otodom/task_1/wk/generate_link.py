import json
import sys


def generate_link():
    with open("settings.json", "r") as f:
        settings = json.load(f)

    # getting base url
    url = settings["base_url"]

    # rent/sale
    rent_sale = settings["for_sale_or_rent"]
    if rent_sale != "None":
        url += (rent_sale + "/")

    # property type
    prop_type = settings["property_type"]
    if prop_type != "None":
        match prop_type:
            case "mieszkania": 
                url += "mieszkanie/"
            case "kawalerki": 
                url += "kawalerka/"
            case "domy": 
                url += "dom/"
            case "inwestycje": 
                url += "inwestycja/"
            case "pokoje": 
                url += "pokoj/"
            case "dzialki": 
                url += "dzialka/"
            case "lokale_uzytkowe": 
                url += "lokal/"
            case "hale_i_magazyny": 
                url += "haleimagazyny/"
            case "garaze": 
                url += "garaz/"
            case _:
                print("invalid value in [property_type] in settings.json!")
                sys.exit(1)

    # province
    province = settings["province"]
    if "-" in province:
        province = province.replace("-", "--")
    if province != "None":
        url += (province + "/")

    # city
    city = settings["city"]
    if city != "None":
        url += (city)

    url += "?"

    # distance_radius
    distance = settings["distance_radius"]
    if distance != "None":
        url += ("?distanceRadius=" + str(distance))

    # price
    min_p = settings["price_min"]
    max_p = settings["price_max"]
    if min_p != "None":
        url += ("&priceMin=" + str(min_p))
    if max_p != "None":
        url += ("&priceMax=" + str(max_p))

    return url


if __name__ == "__main__":
    ans = generate_link()
    print(ans)
