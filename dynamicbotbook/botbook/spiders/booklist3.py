import scrapy

class Booklist3Spider(scrapy.Spider):
    name = "booklist3"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ['https://books.toscrape.com']

    def parse(self, response):
        
        category_links = response.xpath("//div[@class='side_categories']//ul/li/a/@href").getall()
        category_names = response.xpath("//div[@class='side_categories']//ul/li/a/text()").getall()
        
        
        category_names = [name.strip() for name in category_names]
        
        
        category_links = category_links[1:]
        category_names = category_names[1:]
        
        
        for link, name in zip(category_links, category_names):
           
            yield response.follow(link, callback=self.parse_category, meta={'category_name': name})

    def parse_category(self, response):
        
        category = response.meta.get('category_name')
        
       
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
            yield response.follow(next_page, callback=self.parse_category, meta={'category_name': category})
