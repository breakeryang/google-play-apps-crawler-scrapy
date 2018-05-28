# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from gplay.items import MovieItem


class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = [
        # 'https://movie.douban.com/',
        'https://movie.douban.com/subject/27133303/']

    rules = (
        Rule(LinkExtractor(allow=('subject/\d+/.*',)), callback='parse_item'),
    )

    # def parse_start_url(self, response):
    #     self.log("parse start url %s" % response.url)
    #     # for i in self.parse_item(response):
    #     #     yield i
    #     links = response.selector.xpath("//a/@href").extract()
    #     for l in links:
    #         r = self.make_requests_from_url(l)
    #         yield r

    def parse_item(self, response):
        self.logger.info("###%s" % response.url)
        # selector = HtmlXPathSelector(response)
        # name = selector.select('#content > h1 > span:nth-child(1)').extract()
        name = ''.join(response.selector.xpath('//*[@id="content"]/h1/span/text()').extract())
        rating = ''.join(response.selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract())
        i = MovieItem()
        i['name'] = name
        i['rating'] = rating
        return i
