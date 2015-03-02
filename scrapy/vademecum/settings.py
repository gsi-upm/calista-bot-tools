# -*- coding: utf-8 -*-

# Scrapy settings for vademecum project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'vademecum'

SPIDER_MODULES = ['vademecum.spiders']
NEWSPIDER_MODULE = 'vademecum.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'vademecum (+http://www.yourdomain.com)'

FEED_EXPORTERS = {
    'jsonindented' : 'vademecum.exporters.jsonexporter.jsonExporter'
    }