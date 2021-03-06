# -*- coding: utf-8 -*-

# Scrapy settings for lawyers project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import os

DEBUG = os.environ.get("SCRAPYD_DEBUG", False)
if DEBUG:
    LOG_LEVEL='DEBUG'
else:
    LOG_LEVEL='ERROR'
    
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK", None)

BOT_NAME = 'lawyers'

SPIDER_MODULES = ['lawyers.spiders']
NEWSPIDER_MODULE = 'lawyers.spiders'

root_folder = os.environ.get("SCRAPYD_DATADIR", "/tmp/data")
if not os.path.exists("/tmp/data"):
    os.mkdir("/tmp/data")
data_folder = os.path.join(root_folder, BOT_NAME)

FEED_URI=os.path.join(data_folder, "%(name)s.json")
FEED_FORMAT="jsonlines"
FILES_STORE = os.path.join(data_folder, 'files/')
#FEED_EXPORTERS = {
#    'sqlite': 'lawyers.exporters.SqliteItemExporter',
#}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lawyers (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'lawyers.middlewares.JhbBarSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'lawyers.middlewares.JhbBarDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'lawyers.pipelines.MemberDuplicatesPipeline': 300,
    'scrapy.pipelines.files.FilesPipeline' : 400,
}


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 120
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
FEED_EXPORT_ENCODING = 'utf-8'

# Store any local config settings
try:
    from local_settings import *
except ImportError:
    pass
