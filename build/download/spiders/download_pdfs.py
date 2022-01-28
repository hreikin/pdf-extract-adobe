from urllib.request import Request
import scrapy
from download.items import DownloadFilesItem

class DownloadPdfsSpider(scrapy.Spider):
    name = 'download_pdfs'
    allowed_domains = ['princetonscientific.com']
    start_urls = ['https://princetonscientific.com/']

    def parse(self, response):
      for href in response.css("a::attr('href')"):
          url = response.urljoin(href.extract())
          yield scrapy.Request(url, callback = self.parse_page)


    def parse_page(self, response):
        all_links = response.css("a::attr(href)").extract()
        file_extension = ".pdf"
        for link in all_links:
            if file_extension in link:
                url = response.urljoin(link)
                item = DownloadFilesItem()
                item['file_urls'] = [url]
                item['original_filename'] = url.split("/")[-1]
                yield item
