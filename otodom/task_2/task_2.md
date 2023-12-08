
# Task 2 - Refactor
Now since we have already made a simple scraper, we would like our program to be more structrurized and reusable. This is very important in context of any changes of the code in the feature. Thats is why, from now on, we will be using a Object-Oriented-Programming, classes and some principles. By doing that the code will be much simpler to maintain and more readable.
###  Crawler
Create a class ```Crawler``` as following:
```python
class Crawler:
	def __init__(self):
		self.settings = load_settings()
		self.listings = []
		...

	@staticmethod
	def load_settings(...) -> Settings:
		pass

	def generate_url(...) -> str:
		pass

	def count_pages(...) -> int:
		pass

	def get_page(...) -> BeautifulSoup | None:
		pass

	def extract_listings(...) -> list:
		pass

	def crawl(...) -> None:
		pass

```
If you find any other function usefull in context of Crawler don't to hesitate add it.

```load_settings``` - should simply load settings from the ```settings.json``` if such exist if not return some default
```generate_url``` - should be able not only to generate base url for query but also with additional parameter, such as page
```count_pages``` - should return ammount of pages to crawler through
```get_page``` - should return a code of the page already parsed to BS4
```extract_listings``` - should return a list of listings on the page (list of listings pure html code)
```start_scraper``` - should be a place where eveything related to crawling, scraping and so on should take place. We would like to invoke the program from the `main.py` with only creating an instance of Crawler and executing this function.

Regarding static methods check out [this link](https://www.geeksforgeeks.org/class-method-vs-static-method-python/).

###  Settings
`Settings` class should basically represent the settings of our crawler.
```python
class Settings:
	def __init__(self):
		# try to load from settings.json if not possible set some defaults
		...
		self.base_url = ...
		self.price_min = ...
```
### Listing

`Listing` should not only represent a single listings but also should have methods which are strictly related to them. so for example extacting price, are etc.
```python
class Listing:
	def __init__(self, code: str):
		self.price = Listing.extract_price(code)
		self.title = Listing.title(code)
		...

	@staticmethod
	def extract_price(code: str) -> int:
		pass

	@staticmethod
	def extract_title(code: str) -> int:
		pass

```
...and so on

# Docstring

Each of the function/class etc. should have a **docstring**. It must document use-case, summary, parameters, exceptions and return types of the function **DO NOT MAKE CODE COMMENTS FROM NOW ON**. Everything should be put here, **particulary** when code doesn't speak for itself **(it should)**. The example can be seen [here](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html).

For each of the class create corresponding file.

If you have any questions don't hesitate asking.

**Solutions** you can create in the **otodom/task2/<your_name>** file and then make create a pull request.
