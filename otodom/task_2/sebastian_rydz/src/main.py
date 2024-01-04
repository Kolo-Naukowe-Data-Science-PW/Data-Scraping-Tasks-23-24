from crawler import Crawler

if "__main__" == __name__:
    crawler = Crawler()
    crawler.start()
    crawler.to_csv_file("listings.csv")
