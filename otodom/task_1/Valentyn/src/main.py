from Scraper import Scraper
import json

scraper = Scraper()
houseItems = [i.toDictionary() for i in scraper.startScraping(limit=220)]

# Convert the list of dictionaries to a JSON string
json_data = json.dumps(houseItems, indent=4)

# Write the JSON data to a file
with open("data.json", "w") as file:
    file.write(json_data)

print("JSON data has been written to data.json")
