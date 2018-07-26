import scrapy
from urllib import request
from ..items import HaowaiItem

class HaoWaiSpider(scrapy.Spider):
    name = 'haowai'
    start_urls = ['https://www.haowai.com/']
    base_url = 'https://www.haowai.com/'
    custom_settings = {
        "ITEM_PIPELINES" : {
            'haowai.pipelines.HaowaiPipeline': 300,
            'haowai.pipelines.HaoWaiImagePipeline': 1,

        }
    }

    def parse(self, response):
        classUrlList = response.xpath('//div[@class="container-fluidhw-nav"]/nav/span/a/@href').extract()
        for classUrl in classUrlList:
            classUrl = request.urljoin(self.base_url,classUrl)
            yield scrapy.Request(classUrl,callback=self.getClassList)

    def getClassList(self,response):

        url = 'https://www.haowai.com/hajaxUpdateList'
        for i in range(10):
            yield scrapy.Request(url,callback=self.getTrueList,method='POST',dont_filter=True)


    def getTrueList(self,response):
        readNumList = response.xpath('//span[@class="review"]/text()').extract()
        detailUrlList = response.xpath('//div[@class="item-thumbnail"]/div/div/a/@href | //div[@class="caption"]/div/div/div/a/@href').extract()
        # detailTitleList = response.xpath('//div[@class="item-thumbnail"]/div/div/a/@alt | //div[@class="caption"]/div/div/div/a/h3/text()').extract()
        item = HaowaiItem()
        for i in range(len(readNumList)):
            readNum = readNumList[i].strip('阅读')
            # detailTitle = detailTitleList[i]
            item["readNum"] = str(readNum)

            detailUrl = detailUrlList[i]

            detailUrlT = request.urljoin(self.base_url,detailUrl)
            # print(detailUrlT)
            yield scrapy.Request(detailUrlT,callback=self.getDetailCon,meta={'item':item})
        # print('222222222222222222222222222222222222222222222222222222222222222222')
    def getDetailCon(self,response):

        item = response.meta['item']

        # print(item)
        # print('111111111111111111111111111111111111111111111111111111111111111')
        url = response.url
        author = ','.join(response.xpath('//div[@class="author"]/span/span/text()').extract()).strip(' ,')
        puttime = response.xpath('//div[@class="author"]/span/text()').extract()[-1]
        title = response.xpath('//div[@class="article-title"]/h1/text()').extract_first()
        content = ','.join(response.xpath('//div[@class="show-more-snippet"]//text()').extract()).strip(' ,')
        imgUrl = response.xpath('//div[@class="show-more-snippet"]//img/@src').extract()
        print(url)
        print(author)
        print(content)
        item["url"] = url
        item["title"] = title
        item["author"] = author
        item["content"] = content
        item["puttime"] = puttime
        item["imgUrl"] = imgUrl

        yield item


