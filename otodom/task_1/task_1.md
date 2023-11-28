# Otodom
### Task 1
- #### First stage
Let the User provide a link for the page of listings. For example [this one](https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa). You should be able to collect information from the page and create a JSON (dict) from it as following:
```json
{
	"url": "str",
	"otodom_id": "str",
	"title" : "str",
	"localization": {
		"province": "str",
		"city": "str",
		"district": "str",
		"street": "str",
	},
	"promoted": "bool",
	"price": "int",
	"rooms": "int",
	"area": "int",
	"estate_agency": "str"
}
```
If something is missing you can leave the value as an empty string.
* #### Second stage
 The Bot should be able to iterate through all the listings pages. The listings should be again collected and the duplicates should be removed.
### Task 2

Create a **settings.json** file. It should contain things which are going to define what bot is going to scrap. An example may look like:
```json
{
	"base_url": "str",
	"price_min": "str",
	"price_max": "str",
	"city": "str",
	"property_type": "str",
	"only_for_sale": "bool",
	"only_for_rent": "bool",
	...
}
```
and so on. Anything what may be usefull **please try to include**. Dependingly on the data the URL should be somehow generated. Look into Url how the Url is changed accordingly to what search parameters you applied on the site.

**Solutions** you can create in the **pracuj/task1/<your_name>** file and then make create a pull request.
