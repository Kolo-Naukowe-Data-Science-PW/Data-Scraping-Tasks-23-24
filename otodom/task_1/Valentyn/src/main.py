from Scraper import Scraper
from URLConstructor import URLConstructor
import json


target_url = URLConstructor.from_json()
scraper = Scraper(target_url)
house_items = [i.to_dictionary() for i in scraper.start_scraping(limit=100)]

# Convert the list of dictionaries to a JSON string
json_data = json.dumps(house_items, indent=4)

# Write the JSON data to a file
with open("data.json", "w") as file:
    file.write(json_data)

print("JSON data has been written to data.json")
