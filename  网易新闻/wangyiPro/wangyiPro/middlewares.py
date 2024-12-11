from fake_useragent import UserAgent
from time import sleep
from scrapy.http import HtmlResponse

class RandomUserAgentMiddlerware:
    def process_request(self,request,spider):
        '''给每个请求添上一个随机User-Agent'''
        ua = UserAgent()
        request.headers['User-Agent'] = ua.random


class WangyiproDownloaderMiddleware:
    def process_request(self, request, spider):
        '''拦截4个版块的请求'''
        if request.url in spider.model_urls:
            bro = spider.bro
            bro.get(request.url)
            sleep(3)
            # 不断滚动滚动条，直到无法滚动
            current_height = bro.execute_script('return document.body.scrollHeight;')
            while 1:
                bro.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                sleep(3)
                new_height = bro.execute_script('return document.body.scrollHeight;')
                if new_height == current_height:
                    break
                current_height = new_height
            try:
                #页面滚动到底部后，有的需要通过点击'加载更多'按钮来继续加载新闻标题
                bro.find_element_by_css_selector('.post_addmore > span').click()
                sleep(2)
            except:
                pass
            # 返回自己构建的响应
            return HtmlResponse(url=bro.current_url,body=bro.page_source,request=request,encoding='utf-8')