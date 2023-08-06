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

        self.pipe["readme"] = result[0] if result else False

        yield {
            "extracted": response.request.url,
            "success": bool(result)
        }
