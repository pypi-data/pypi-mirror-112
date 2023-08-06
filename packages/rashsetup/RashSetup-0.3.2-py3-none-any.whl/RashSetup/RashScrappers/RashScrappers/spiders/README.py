import scrapy


class ReadmeSpider(scrapy.Spider):
    name = 'README'
    allowed_domains = ['github.com']

    def __init__(
            self, pipe, url
    ):
        super().__init__()

        self.start_urls = url
        self.pipe = pipe

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls, errback=self.error_pipe
        )

    def error_pipe(self, *args):
        self.pipe["failed"] = True
        self.pipe["exception"] = str(args[0])
        self.pipe["result"] = False

    def parse(self, response, *args):
        got = response.xpath("//div[@id='readme']")

        result = got.extract()

        self.pipe["result"] = result[0] if result else False
        self.pipe["failed"] = not bool(result[0])
        self.pipe["exception"] = ""

        yield {
            "extracted": response.request.url,
            "success": bool(result)
        }
