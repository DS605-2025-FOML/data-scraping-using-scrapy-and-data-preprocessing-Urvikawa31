import scrapy 
from ..items import Assignment1Item 
class QuotesSpider(scrapy.Spider): 
    name = "books"  
    start_urls = [ 
        'https://books.toscrape.com/catalogue/page-1.html', 
    ] 
 
    def parse(self, response):  
     
        all_books = response.css('article.product_pod') 
         
        for book in all_books:
            items = Assignment1Item()
            items['book_name'] = book.css('h3 a::attr(title)').extract()
            items['price'] = book.css('p.price_color::text').extract()
            items['availability'] = ''.join(book.css('p.availability::text').getall()).strip()
            items['rating'] = book.css('p::attr(class)').re_first('star-rating\s+(\w+)')
 
            yield items 
  
        next_page = response.css('li.next a::attr(href)').get() 
 
        if next_page is not None: 
            yield response.follow(next_page, callback=self.parse)