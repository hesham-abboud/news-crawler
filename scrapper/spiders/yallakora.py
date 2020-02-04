# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
from newsplease import NewsPlease
from ..models.article import Article
from ..models.news_repo import NewsRepo


class YallakoraSpider(scrapy.Spider):
    name = 'yallakora'
    allowed_domains = ['yallakora.com']
    start_urls = ['https://www.yallakora.com/NewsListing/']
    base_url = "https://www.yallakora.com"
    news_repo = None

    def __init__(self):
        self.news_repo = NewsRepo()

    def parse(self, response):
        page = response.url.split("/")[-2]
        links = response.css('div.cnts a.link::attr(href)').getall()

        for link in links:
            print("links: ", link)
            yield response.follow(link, callback=self.parse_article_custom)

    def parse_article_newsplease(self, link):
        article = NewsPlease.from_url(self.base_url + link)
        return article.get_dict()

    def parse_article_custom(self, response):
        article = Article()

        article.title = response.css('h1.artclHdline::text').get()
        article.author = response.css(
            'div.articleAuthor p span::text').get().strip()
        article.date = response.css(
            'div.time span::text').getall()[0].strip()
        article.time = response.css(
            'div.time span::text').getall()[1].strip()
        article.content = ' '.join(response.css(
            'div.ArticleDetails p::text').getall())
        article.url = response.url
        article.tags = response.css('div.keywordsDiv a.item::text').getall()
        article.source = "yallakora"
        article.generate_id()

        #print("article: ", article.__dict__)
        self.news_repo.insert_news(article)

    def myconverter(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    def __del__(self):
        self.news_repo.close_conn()
