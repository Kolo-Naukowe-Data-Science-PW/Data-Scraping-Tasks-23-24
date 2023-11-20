# Pracuj
### Task 1
- #### First stage
Let the User provide a link for the page of listings. For example [this one](https://www.pracuj.pl/praca/warszawa;wp?rd=30&cc=5016%2C5015&sal=1). **We only want to fetch listings with a given salary range.** You should be able to collect information from the page and create a JSON (dict) from it as following:
```json
{
	"url": "str",
	"pracuj_id": "str",
	"title" : "str",
	"company": "str",
	"type_of_contract": "list[str]",
	"salary": "int",
	"specialization": "str",
	"operating_mode": "list[str]",
	"promoted": "bool",
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
	"salary_min": "str",
	"salary_max": "str",
	"city": "str",
	"category": "str",
	...
}
```
and so on. Anything what may be usefull **please try to include**. Start with the most important things. Dependingly on the data the URL should be somehow generated. Look into Url how the Url is changed accordingly to what search parameters you applied on the site.

**Solutions** you can create in the **pracuj/task1/<your_name>** file and then make create a pull request.