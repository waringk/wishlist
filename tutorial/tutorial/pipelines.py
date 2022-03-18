# Citation for the file:
# This file is boilerplate code from https://docs.scrapy.org
# Date: 3/12/2022
# Source URL: https://docs.scrapy.org/en/latest/intro/install.html


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TutorialPipeline:
    def process_item(self, item, spider):
        for k, v in item.items():
            if not v:
                item[k] = ''  # replace empty list or None with empty string
                continue
            if k == 'Title':
                item[k] = v.strip()
            elif k == 'Rating':
                item[k] = v.replace(' out of 5 stars', '')
            elif k == 'AvailableSizes' or k == 'AvailableColors':
                item[k] = ", ".join(v)
            elif k == 'BulletPoints':
                item[k] = ", ".join([i.strip() for i in v if i.strip()])
            elif k == 'SellerRank':
                item[k] = " ".join([i.strip() for i in v if i.strip()])
        return item