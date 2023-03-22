import scrapy

LINKS_TO = '//a[starts-with(@href,"collection") and (parent::h3|parent::h2)]/@href'
TITLE_ART = '//h1[@class="documentFirstHeading"]/text()'
SUMMARY_ART = '//div[@class="field-item even"]/p[not(@style)]/text()'




class SpiderCia(scrapy.Spider):
    name = 'ciaspider'
    start_urls = [
        'https://www.cia.gov/readingroom/historical-collections'
    ]
    custom_settings = {
        'FEED_URI' : 'cia.json',
        'FEED_FORMAT' : 'json',
        'FEED_EXPORT_ENCODING' : 'utf-8'
    }



    def parse(self, response):
        links = response.xpath(LINKS_TO).getall()
        for link in links:
            yield response.follow(link, callback = self.parse_info, cb_kwargs={'url':response.urljoin(link)})

    def parse_info(self,response, ** kwargs):
        url = kwargs['url']
        title = response.xpath(TITLE_ART).get()
        summary = response.xpath(SUMMARY_ART).get()
        yield {
            "Adress":url,
            "Title":title,
            "Summary":summary
        }
