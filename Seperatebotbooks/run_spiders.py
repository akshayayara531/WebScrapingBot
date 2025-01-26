from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


from bot_book1.bot_book1.spiders.travel_booklist import TravelBooklistSpider  # Replace with actual spider imports
from bot_book2.bot_book2.spiders.fiction_booklist import FictionBooklistSpider


process = CrawlerProcess(settings=get_project_settings())
process.settings.set('FEED_URI', 'output.csv')  
process.settings.set('FEED_FORMAT', 'csv')

process.crawl(TravelBooklistSpider,output='output.csv')
process.crawl(FictionBooklistSpider, output='output.csv')


process.start()
