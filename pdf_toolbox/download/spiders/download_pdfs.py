import logging, scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from download.items import DownloadFilesItem

class DownloadPdfsSpider(scrapy.Spider):
    """Spider for scraping a full website downloading PDF files."""
    name = 'download_pdfs'
    allowed_domains = []
    start_urls = []

    def parse(self, response):
        """Finds all links in a page and creates a request."""
      for href in response.css("a::attr('href')"):
          url = response.urljoin(href.extract())
          yield scrapy.Request(url, callback = self.parse_page)


    def parse_page(self, response):
        """Parses all links in a page and looks for PDF file extensions that are 
        then passed to the download pipeline."""
        all_links = response.css("a::attr(href)").extract()
        file_extension = ".pdf"
        for link in all_links:
            if file_extension in link:
                url = response.urljoin(link)
                item = DownloadFilesItem()
                item['file_urls'] = [url]
                item['original_filename'] = url.split("/")[-1]
                item['page'] = response.url
                yield item

def run_spider(allowed_domain, start_url):
    """Creates a process with the crawlers settings and starts it."""
    spider_process = CrawlerProcess(get_project_settings())
    spider_process.crawl(DownloadPdfsSpider, start_urls=[start_url], allowed_domains=[allowed_domain])
    spider_process.start()
    logging.info("Crawling finished.")
