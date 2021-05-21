import scrapy

class BlogSpider(scrapy.Spider):
    # name of the spider
    name = "blog"

    def start_requests(self):
        # return an iterable of Requests 
        # (you can return a list of requests 
        # or write a generator function) which the Spider will begin to crawl from
        
        # urls we want to crawl
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            # yield return a iterable of requests
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Callback function: what we gonna do with the data crawled
        title = response.xpath('//title/text()').get()

        with open("output.txt", 'wb') as f:
            f.write(title)
