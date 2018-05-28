# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from gplay.items import MovieItem


class ZhihuSpider(CrawlSpider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = [
        # 'https://movie.douban.com/',
        'https://www.zhihu.com/question/57307108'
    ]

    rules = (
        Rule(LinkExtractor(allow=('question/\d+.*',)), callback='parse_item', follow=True),
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
        name = ''.join(
            response.selector.xpath('//div/@data-zop-question').extract())
        rating = ''.join(response.selector.xpath(
            '//*[@id="root"]/div/main/div/div[1]/div[2]/div[1]/div[2]/div/div/div/button/div/strong/text()').extract())
        i = MovieItem()
        i['name'] = name
        i['rating'] = rating
        return i
