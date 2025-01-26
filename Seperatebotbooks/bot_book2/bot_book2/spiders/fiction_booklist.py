import scrapy


class FictionBooklistSpider(scrapy.Spider):
    name = "fiction_booklist"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/category/books/fiction_10/index.html"]

    def parse(self, response):
       
        category=response.xpath("//h1/text()").get()

        
       
        for book in response.xpath("//article[@class='product_pod']"):
            rating = book.xpath(".//p[@class]/@class").get()
            title = book.xpath(".//h3/a/@title").get()
            price = book.xpath(".//div[@class='product_price']/p[@class='price_color']/text()").get()
            
            if rating:
                rating = rating.split()[-1] + ' star'
            
            availability = book.xpath(
                "string(.//div[@class='product_price']/p[@class='instock availability'])"
            ).get().strip()

            yield {
                'category': category,
                'title': title,
                'price': price,
                'rating': rating,
                'availability': availability,
            }

        
        next_page = response.xpath("//div/ul[@class='pager']/li[@class='next']/a/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
