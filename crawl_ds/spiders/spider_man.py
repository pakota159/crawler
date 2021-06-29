import scrapy
import logging
import csv
import re

class BlogSpider(scrapy.Spider):
    # Setup log for this spider.
    # def __init__(self, *args, **kwargs):
    #     logger = logging.getLogger('scrapy')
    #     logger.setLevel(logging.ERROR)
    #     super().__init__(*args, **kwargs)
    
    # name of the spider
    name = "blog"

    def start_requests(self):
        # return an iterable of Requests 
        # (you can return a list of requests 
        # or write a generator function) which the Spider will begin to crawl from
        
        # urls we want to crawl
        urls = []

        with open('./data_cleaning/links.txt', mode='r') as links:
            lines = links.readlines()
            for line in lines:
                urls.append(line.strip())
        
        self.init_file()

        for url in urls:
            # yield return a iterable of requests
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Callback function: what we gonna do with the data crawled

        # Get all paragraphs
        p_tags = response.css("p::text")
        title_text = response.css("title::text").get().strip()

        for p_tag in p_tags:
            cleaned_para = self.cleaning(p_tag.get())
            if cleaned_para:
                self.write_file(title_text, cleaned_para)
                print("Done: " + title_text)
            
    def cleaning(self, para):
        splited = para.strip().split(".")
        splited = list(filter(
            lambda x: len(x) > 0 and x.strip()[0] == x.strip()[0].upper() and bool(re.match(r"[A-z0-9]", x.strip()[0])), splited
        ))
        if (len(splited) > 2):
            text = ".".join(splited)
            return text.strip()
    
    def init_file(self):
        with open('./data_cleaning/raw_data.csv', mode='w') as raw_data:
            writer = csv.writer(raw_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['title', 'paragraph'])

    def write_file(self, title, para):
        with open('./data_cleaning/raw_data.csv', mode='a') as raw_data:
            writer = csv.writer(raw_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([title, para])


class LinkSpider(scrapy.Spider):
    name = "link"

    def start_requests(self):
        urls = [
            # 'https://www.kdnuggets.com/tag/data-science',
            # 'https://www.kdnuggets.com/tag/data-science/page/2',
            # 'https://www.kdnuggets.com/tag/data-science/page/3',
            # 'https://www.kdnuggets.com/tag/data-science/page/4',
            # 'https://www.kdnuggets.com/tag/data-science/page/5',
            # 'https://www.kdnuggets.com/tag/data-science/page/6',
            # 'https://www.kdnuggets.com/tag/data-science/page/7',
            # 'https://www.kdnuggets.com/tag/data-science/page/8',
            # 'https://www.kdnuggets.com/tag/data-science/page/9',
        ]

        for i in range(1,20):
            urls.append('https://simplystatistics.org/page/{}/'.format(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Get all paragraphs
        if 'simplystatistics' in response.url:
            for article in response.css("article"):
                raw_link = article.css("header h2 a::attr(href)").get()
                link = 'https://simplystatistics.org' + raw_link[raw_link.index('./20')+1:]
                if 'episode' not in link:
                    print(link)

        # for li in response.css("ul.three_ul li"):
        #     a_tag = li.css("a::attr(href)").get()
        #     if bool(re.search(r"\/20[0-9]{2}\/[0-9]{2}\/", a_tag)):
        #         with open('links.txt', 'a') as the_file:
        #             the_file.write(a_tag + "\n")