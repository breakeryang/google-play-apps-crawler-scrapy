# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from gplay.items import GplayItem
import urlparse


class GooplaySpider(CrawlSpider):
    # def parse(self, response):
    #     pass

    name = 'gooplay'
    allowed_domains = ["play.google.com"]
    start_urls = ["https://play.google.com/store/apps/"]
    rules = (
        Rule(LinkExtractor(allow=('/store/apps',)), follow=True),
        Rule(LinkExtractor(allow=('/store/apps/details\?')), follow=True, callback='parse_link')
    )

    def abs_url(url, response):
        """Return absolute link"""
        base = response.xpath('//head/base/@href').extract()
        if base:
            base = base[0]
        else:
            base = response.url
        return urlparse.urljoin(base, url)

    def parse_link(self, response):

        title = response.selector.xpath('//*[@itemprop="name"]/span/text()').extract()

        self.logger.info("parse PKG %s" % title)
        # hxs = HtmlXPathSelector(response)
        # titles = hxs.select('/html')
        # items = []
        # for titles in titles:
        item = GplayItem()
        item["Link"] = response.selector.xpath('head/link[5]/@href').extract()
        # item["Item_name"] = response.selector.xpath('//*[@class="document-title"]/div/text()').extract()
        item["Updated"] = response.selector.xpath('//*[@itemprop="datePublished"]/text()').extract()
        item["Author"] = response.selector.xpath('//*[@itemprop="author"]/a/span/text()').extract()
        item["Title"] = response.selector.xpath('//*[@itemprop="name"]/span/text()').extract()
        item["Filesize"] = response.selector.xpath('//*[@itemprop="fileSize"]/text()').extract()
        item["Downloads"] = response.selector.xpath('//*[@itemprop="numDownloads"]/text()').extract()
        item["Version"] = response.selector.xpath('//*[@itemprop="softwareVersion"]/text()').extract()
        item["Compatibility"] = response.selector.xpath('//*[@itemprop="softwareVersion"]/text()').extract()
        item["Content_rating"] = response.selector.xpath('//*[@itemprop="contentRating"]/text()').extract()
        item["Author_link"] = response.selector.xpath('//*[@class="dev-link"]/@href').extract()
        item["Author_link_test"] = response.selector.xpath('//*[@class="content contains-text-link"]/a/@href').extract()
        item["Genre"] = response.selector.xpath('//*[@itemprop="genre"]/text()').extract()
        item["Price"] = response.selector.xpath('//*[@class="price buy id-track-click"]/span[2]/text()').extract()
        item["Rating_value"] = response.selector.xpath('//*[@class="score"]/text()').extract()
        item["Review_number"] = response.selector.xpath('//*[@class="reviews-num"]/text()').extract()
        item["Description"] = response.selector.xpath('//*[@class="id-app-orig-desc"]//text()').extract()
        item["IAP"] = response.selector.xpath('//*[@class="inapp-msg"]/text()').extract()
        item["Developer_badge"] = response.selector.xpath('//*[@class="badge-title"]//text()').extract()
        item["Physical_address"] = response.selector.xpath('//*[@class="content physical-address"]/text()').extract()
        item["Video_URL"] = response.selector.xpath('//*[@class="play-action-container"]/@data-video-url').extract()
        item["Developer_ID"] = response.selector.xpath('//*[@itemprop="author"]/a/@href').extract()
        # items.append(item)
        return item
