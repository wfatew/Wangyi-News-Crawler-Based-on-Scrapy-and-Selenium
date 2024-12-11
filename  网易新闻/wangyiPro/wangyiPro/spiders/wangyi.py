import scrapy
import os
import logging
from wangyiPro.items import WangyiproItem  # 忽略该错误
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    allowed_domains = ['163.com']
    start_urls = ['https://news.163.com/']
    model_urls = []  # 用于存储国内、国际、军事和航空4个版块的url

    def __init__(self):
        # 指定 ChromeDriver 路径
        logging.info("Initializing browser...")
        service = Service('chromedriver.exe')  # 替换为实际路径
        self.bro = webdriver.Chrome(service=service)  # 创建浏览器对象
        logging.info("Browser initialized.")

    def parse(self, response):
        '''解析首页'''

        # 创建目录:网易新闻
        if not os.path.exists('网易新闻'):
            os.mkdir('网易新闻')
        li_list = response.xpath('//div[@class="ns_area list"]/ul/li')
        index_list = [1, 2, 4, 5]  # 国内、国际、军事和航空4个版块对应的索引
        for index in index_list:
            li = li_list[index]
            # 获取这4个版块的url和名称
            model_url = li.xpath('./a/@href').extract_first()
            model_name = li.xpath('./a/text()').extract_first()
            self.model_urls.append(model_url)
            # 存储新闻的路径
            path = '网易新闻/' + model_name
            # 在目录:网易新闻下继续按照各版块名新建目录
            if not os.path.exists(path):
                os.mkdir(path)
            # 初始化每个版块的计数器
            yield scrapy.Request(url=model_url, callback=self.parse_model, meta={'path': path, 'counter': 0})

    def parse_model(self, response):
        '''解析各版块页'''

        path = response.meta.get('path')
        counter = response.meta.get('counter')  # 获取当前计数器
        div_list = response.xpath('//div[contains(@class,"data_row")]')
        for div in div_list:
            if counter >= 3:  # 限制每个版块最多3条数据
                break

            detail_title = div.xpath('.//h3/a/text()').extract_first()
            detail_url = div.xpath('.//h3/a/@href').extract_first()
            # 实例化item对象
            item = WangyiproItem()
            item['title'] = detail_title
            item['path'] = path
            counter += 1  # 更新计数器

            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'item': item, 'counter': counter, 'path': path})

    def parse_detail(self, response):
        '''解析详情页'''

        item = response.meta.get('item')

        # 尝试多种选择器提取内容
        content_list = response.css('.post_body p::text').extract()
        if not content_list:
            # 如果第一个选择器无效，尝试其他可能的选择器
            content_list = response.css('.content p::text').extract()
        if not content_list:
            # 如果仍无效，尝试更通用的选择器
            content_list = response.xpath('//p/text()').extract()

        content = '\n'.join(content_list)  # 将内容拼接成字符串
        if content.strip():  # 确保内容非空
            item['content'] = content
            yield item
        else:
            # 如果没有提取到内容，记录日志
            self.logger.warning(f"Content not found for URL: {response.url}")

    @staticmethod
    def close(spider, reason):
        '''关闭浏览器'''
        spider.bro.quit()
