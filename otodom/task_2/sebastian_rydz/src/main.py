from crawler import Crawler

if "__main__" == __name__:
    crawler = Crawler()
    crawler.start()
    crawler.save_to_file("listings.json")
