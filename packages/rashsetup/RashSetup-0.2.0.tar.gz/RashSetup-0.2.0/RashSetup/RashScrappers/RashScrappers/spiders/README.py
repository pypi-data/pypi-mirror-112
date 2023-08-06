import scrapy


class ReadmeSpider(scrapy.Spider):
    name = 'README'
    allowed_domains = ['github.com']

    def __init__(
            self, pipe, url
    ):
        super().__init__()

        self.start_urls = [
            url
        ]
        self.pipe = pipe

    def parse(self, response, *args):
        got = response.xpath("//div[@id='readme']")

        result = got.extract()

        self.pipe.put(
            bool(result)
        )

        self.pipe.put(
            result[0] if result else f"Failed to request README.md from {response.request.url}"
        )

        yield {
            "extracted": response.request.url
        }


if __name__ == "__main__":
    import scrapy.crawler

    process = scrapy.crawler.CrawlerProcess()
    pipe = []
    process.crawl(ReadmeSpider, url="https://github.com/RahulARanger/Rash/blob/master/README.md", pipe=pipe)
    process.start()

    print(pipe)


