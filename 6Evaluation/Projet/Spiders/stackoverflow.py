import scrapy
import json
import os
import time

class StackoverflowSpider(scrapy.Spider):
    name = 'stackoverflow'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions?tab=Frequent' + "&page=" + str(i) for i in range(30000)]
    cpt = 0
    f = open("data.csv","w",encoding='utf-8')
    f.write("title;votes;answers;time;views;tags;author\n")
    def parse(self, response):
        for elt in response.css('div.question-summary'):
            self.cpt = self.cpt + 1
            title = elt.css('h3').css("a::text").extract()[0]
            votes, answers = elt.css('.statscontainer').css('strong::text').extract(); votes = int(votes); answers = int(answers)
            ti = elt.css('span.relativeti::attr(title)').extract()
            if len(ti) != 0 : ti = ti[0] 
            else : ti = None
            views = elt.css('div.views::attr(title)').extract()[0]; views = int(views.replace(" views","").replace(",",""))
            tags = elt.css('a.post-tag::text').extract()
            author = elt.css('div.user-details').css('a::text').extract()
            if len(author) != 0 : author = author[-1]
            else : author = None
            title = title.replace(";",":")
            query = repr(str(title))+";"+repr(str(votes))+";"+repr(str(answers))+";"+repr(str(ti))+";"+repr(str(views))+";"+repr(str(tags))+";"+repr(str(author))+"\n"
            self.f.write(query)
            time.sleep(0.5)
