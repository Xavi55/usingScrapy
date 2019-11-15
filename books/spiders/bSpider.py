# -*- coding: utf-8 -*-
import scrapy
from books.items import BooksItem
from collections import OrderedDict

##pages=int(input('how many pages?'))
##conv={'One':1,'Two':2,'Three':3,'Four':4,'Five':5}
class BspiderSpider(scrapy.Spider):
    name = 'bSpider'
    COUNT=0
    LIMIT=1
    start_urls = [
        #using iterative pagination
        #'http://books.toscrape.com/catalogue/page-{}.html'.format(i+1) for i in range(pages)
        'http://books.toscrape.com/catalogue/page-1.html'
        ]

    def parse(self, response):
        data=OrderedDict(BooksItem())
        books=response.css('ol.row')
        for book in books:
            for b in book.css('article.product_pod'):
                data['title']=b.css('a::attr(title)').getall()
                
                '''
                #without import items  
                
                data['title']=b.css('a::attr(title)').getall()
                data['price']=b.css('div.product_price p.price_color::text').getall()
                data['stock']=b.css('div.product_price p.instock.availability::text').getall()[1].strip()
                data['rating']=conv[b.css('p::attr(class)').getall()[0].split()[-1]]
                '''
                yield data

        nextPage=response.css('li.next a::attr(href)').getall()
        if self.COUNT < self.LIMIT:
            nextLink=response.urljoin(nextPage[0]) 
            self.COUNT+=1
            yield scrapy.Request(url=nextLink,callback=self.parse)

