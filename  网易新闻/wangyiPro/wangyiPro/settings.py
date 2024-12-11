BOT_NAME = 'wangyiPro'

SPIDER_MODULES = ['wangyiPro.spiders']
NEWSPIDER_MODULE = 'wangyiPro.spiders'

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 2 #设置下载延迟

#开启下载中间件
DOWNLOADER_MIDDLEWARES = {
   'wangyiPro.middlewares.RandomUserAgentMiddlerware':600,
   'wangyiPro.middlewares.WangyiproDownloaderMiddleware': 543,
}

#开启管道
ITEM_PIPELINES = {
   'wangyiPro.pipelines.WangyiproPipeline': 300,
}

#设置log级别
LOG_LEVEL = 'ERROR'