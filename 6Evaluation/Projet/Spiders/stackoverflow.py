import scrapy
import json
import os


class StackoverflowSpider(scrapy.Spider):
    name = 'stackoverflow'
    allowed_domains = ['https://stackoverflow.com/questions?tab=Frequent']
    start_urls = ['https://stackoverflow.com/questions?tab=Frequent' + "&page=" + str(i) for i in range(5)]
    cpt = 0
    f = open("data.json","w")
    d = {}

    def parse(self, response):
        for elt in response.css('div.question-summary'):
            self.cpt = self.cpt + 1
            title = elt.css('h3').css("a::text").extract()[0]
            votes, answers = elt.css('.statscontainer').css('strong::text').extract(); votes = int(votes); answers = int(answers)
            time = elt.css('span.relativetime::attr(title)').extract()
            if len(time) != 0 : time = time[0] 
            else : time = None
            views = elt.css('div.views::attr(title)').extract()[0]; views = int(views.replace(" views","").replace(",",""))
            tags = elt.css('a.post-tag::text').extract()
            author = elt.css('div.user-details').css('a::text').extract()
            if len(author) != 0 : author = author[-1]
            else : author = None
            self.d[str(elt)] = {
                "title" : title,
                "votes" : votes,
                "answers" : answers,
                "time" : time,
                "views" : views,
                "tags" : tags,
                "author" : author
            }
            json.dump(self.d,self.f,indent=2,separators=(', ',': '))

        print(len(self.d))                
