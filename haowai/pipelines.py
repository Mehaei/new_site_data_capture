# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class HaowaiPipeline(object):
    def open_spider(self,spider):
        self.db = pymysql.connect('127.0.0.1','root','123456','reptile',charset="utf8")
        self.cursor = self.db.cursor()
    def process_item(self, item, spider):
        sql = 'insert into haowai(url,title,author,content,puttime,readnum,imagepath) values(%s,%s,%s,%s,%s,%s,%s)'
        data = (item['url'],item['title'],item['author'],item['content'],item['puttime'],item['readNum'],item['imagePath'])
        try:
            self.cursor.execute(sql,data)
            self.db.commit()
        except Exception as e:
            # 插入失败则将主键自增设置为1，否则插入数据失败id也会自增，就会出现主键增长不连续的情况
            self.cursor.execute('alter table haowai auto_increment=1')
            self.db.rollback()
            print('存储失败',e)

        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()


from scrapy.pipelines.images import ImagesPipeline
class HaoWaiImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        print('经过了图片下载',results)
        # 经过了图片下载 [(True, {'url': 'http://img.hwoutput.com/upload/article/cache/20180705/F2M64NAICQ_2bee4eb8c6f3fa882fecc44c007256d5.jpg?x-oss-process=style/wm', 'path': 'full/05879ddda8717c22a7f2103325992763bc64796d.jpg', 'checksum': '9b6f56af218d8f43a8e67d809df8e5c7'}), (True, {'url': 'http://img.hwoutput.com/upload/article/cache/20180705/F2M64NAICQ_1648c92b903589d023ab1e7702403dda.jpg?x-oss-process=style/wm', 'path': 'full/f846dc6ba97aa634a491fcf6256eefc7018b2dc5.jpg', 'checksum': 'f0a8f2bf18e8c12579f31f9e72b38ee3'}), (True, {'url': 'http://img.hwoutput.com/upload/article/cache/20180705/F2M64NAICQ_b0cc7e4f2a17df6666b5b6f5677db290.jpg?x-oss-process=style/wm', 'path': 'full/b9380ba1320ff644e44bf6ea02aae034948a2b21.jpg', 'checksum': 'f50006023065d1776827b2dcc288b3b5'}), (True, {'url': 'http://img.hwoutput.com/upload/article/cache/20180705/F2M64NAICQ_65d946bd013590ebe41b11262cba9250.jpg?x-oss-process=style/wm', 'path': 'full/347c7c3df2e43597301fefd690bcee4deddf12c5.jpg', 'checksum': '570590ef99aa4059e175abc49c08ae5a'}), (True, {'url': 'http://img.hwoutput.com/upload/article/cache/20180705/F2M64NAICQ_497fbff392bdb3449c5f6b3ef3093c34.jpg?x-oss-process=style/wm', 'path': 'full/4807062d2025ea3cd6ec19ce740800f9b7a50a61.jpg', 'checksum': '97fafe408bcc9bced08e8dc18a6adf2e'}), (True, {'url': 'http://img.hwoutput.com/upload/article/cache/20180705/F2M64NAICQ_d6178f8a10a6f7eb6024e0771669ebc9.jpg?x-oss-process=style/wm', 'path': 'full/81c3b6b7ce4e7c40427fb320253e12bdfd556064.jpg', 'checksum': '73466742d30401b187738c5a05f8c97f'}), (True, {'url': 'http://img.hwoutput.com/upload/article/cache/20180705/F2M64NAICQ_8a04a977e70d845904f9c8e18076660f.jpg?x-oss-process=style/wm', 'path': 'full/7c044deb5e177fac9d5d2862870f7f8a7fe9acb2.jpg', 'checksum': '579682f6d98d277a65430ecb1b159dbb'}), (True, {'url': 'http://img.hwoutput.com/upload/article/cache/20180705/F2M64NAICQ_a11a47e4f04402fab39975ca880b9a1a.jpg?x-oss-process=style/wm', 'path': 'full/80c477f7819d390d3b09331a86e536eac64ba974.jpg', 'checksum': 'eceb265e7c109ea89f8dbc51c84e3ce8'})]
        # item['imagePath'] = '23'

        img_path = []
        for res in results:
            if res[0]: # 下载成功
                path = res[1]['path'].strip('full/')
                img_path.append(path)

        img_path = ','.join(img_path)
        item['imagePath'] = img_path

        return item
