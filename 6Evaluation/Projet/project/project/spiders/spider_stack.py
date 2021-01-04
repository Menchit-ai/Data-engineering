import scrapy
from ..items import ProjectItem
from scrapy import Request

class StackoverflowSpider(scrapy.Spider):
    name = 'stack'
    start_urls = ['https://stackoverflow.com/questions?tab=frequent&pagesize=50']

    def parse(self, response):

        nb_pages = max( map( int,response.css('div.s-pagination').css('a.js-pagination-item::text').extract()[:-1] ) )
        urls = ['https://stackoverflow.com/questions?tab=Frequent&pagesize=50&page='+ str(i) for i in range(1,nb_pages+1) ]

        for next_url in urls:
            yield Request(next_url, callback=self.parse_page)

    def parse_page(self, response):
        items = ProjectItem()

        for elt in response.css('div.question-summary'):
            title = elt.css('h3').css("a::text").extract()[0]
            votes, answers = elt.css('.statscontainer').css('strong::text').extract()
            date = elt.css('span.relativetime::attr(title)').extract()
            if len(date) != 0 : date = date[0]
            else : date = None
            views = elt.css('div.views::attr(title)').extract()[0]; views = int(views.replace(" views","").replace(",",""))
            tags = elt.css('a.post-tag::text').extract()
            author = elt.css('div.user-details').css('a::text').extract()
            if len(author) != 0 : author = author[-1]
            else : author = None

            items['title'] = title
            items['votes'] = votes
            items['answers'] = answers
            items['date'] = date
            items['views'] = views
            items['tags'] = tags
            items['author'] = author
            
            yield items
