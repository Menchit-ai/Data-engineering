import scrapy


class StackoverflowSpider(scrapy.Spider):
    name = 'stackoverflow'
    allowed_domains = ['https://stackoverflow.com/questions?tab=Bounties']
    start_urls = ['http://https://stackoverflow.com/questions?tab=Bounties/']

    def parse(self, response):
        for elt in response.css('div.question-summary'):
        	title = elt.css('h3').css("a::text").extract()
        	votes = elt.css('span.vote-count-post::attr(title)').extract()
        	answers = elt.css('div.status.answered').css('strong::text').extract()
        	time = elt.css('span.relativetime::attr(title)').extract()
        	views = elt.css('div.views::attr(title)').extract()
        	tags = elt.css('a.post-tag::text').extract()
        	author = elt.css('div.user-details').css('a::text').extract()

        	print(title + '\n' + votes + '\n' + answers + '\n' + time + '\n' + views + '\n' + tags + author)

