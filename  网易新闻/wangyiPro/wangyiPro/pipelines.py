class WangyiproPipeline:
    def process_item(self, item, spider):
        file_name = item['path']+'/'+item['title']+'.txt'
        with open(file_name,'w',encoding='utf-8') as f:
            f.write(item['content'])
        return item