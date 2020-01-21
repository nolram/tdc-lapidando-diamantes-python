# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news_crawler.items import Article

__author__ = 'nolram'


class ArticleSpiderTecnoBlog(CrawlSpider):

    name = "tecnoblog"
    allowed_domains = ["tecnoblog.net", "tecnoblog.net"]
    start_urls = ["https://tecnoblog.net/"]

    rules = (
        Rule(LinkExtractor(allow=('(.+)(/[0-9]+/)(.+)/$', ),
                           deny=('(.+)(/categoria/)(/podcast/)',)),
             callback='parse_item', follow=True,),
    )

    def parse_item(self, response):
        item = Article()

        titulo = response.xpath('//article[@id="post"]//h1//a/text()').extract_first()

        subtitulo = response.xpath('//article[@id="post"]//h2/text()').extract_first()

        texto = response.xpath('//article[@id="post"]//div[@class="grid8"]//p/text()').extract()

        autor = response.xpath('//article[@id="post"]//header//div//div[@class="by"]//span//span[@class="author"]//a/text()'
                               ).extract_first()

        data_publicacao = response.xpath('//article[@id="post"]//div[@class="by"]//span/text()').extract()

        if titulo:
            item["titulo"] = titulo
        if subtitulo:
            item["subtitulo"] = subtitulo

        if data_publicacao:
            item["data_publicacao"] = data_publicacao[-1].replace("\n", "").strip()

        if autor:
            item["autor"] = autor

        if texto:
            item["texto"] = " ".join(texto)

        item["url"] = response.url

        yield item
