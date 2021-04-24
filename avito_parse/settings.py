# Scrapy settings for avito_parse project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'avito_parse'

SPIDER_MODULES = ['avito_parse.spiders']
NEWSPIDER_MODULE = 'avito_parse.spiders'

LOG_ENABLE = True
LOG_LEVEL = "DEBUG"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Cookie': '__cfduid=d233c40546f1488e67f41d5b8d921b0b51619277487; _gcl_au=1.1.590412304.1619277487; u=2oo13unz.1n4jyoi.1fsz02yaqna00; v=1619277487; _ga=GA1.2.209256664.1619277487; _gid=GA1.2.1880423002.1619277487; _fbp=fb.1.1619277487394.952017769; f=5.32e32548b6f3e9784b5abdd419952845a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36c1e8912fd5a48d02c1e8912fd5a48d0246b8ae4e81acb9fa1a2a574992f83a9246b8ae4e81acb9fad99271d186dc1cd0e992ad2cc54b8aa…joxNjIwNDg3MTQ1fQ.jB5wGo3FmqhEH4IB_hwHhSNNZtNiFWcsz02t5Ls2W3Y; _ym_uid=1619277546316026447; _ym_d=1619277546; __gads=ID=b8a87cf2e9db9bbd-2295e861f0c70049:T=1619277546:S=ALNI_MZ7eb-VgnGfC9EzFMQnZpWs6zWpNQ; _ym_isad=2; cto_bundle=bJRpK191Y1NFY2p0OXY5V3hkdW5KRTlubEE4czkyaDRFeUxjU21RZFZINzU0R1h0NTBxaEZjMTRRcllTck5OcmRycXdqUHAwTUJzY1NjY0hzREdyQjlwMFR6dkglMkYyNzhXNjgwJTJGUjN2Mm5rbGVGRyUyQjJHZWNmeG1DRVAlMkZNV01GeUNEV0VUaEtvRTVsY09WYlNQM3MlMkZKVW9CJTJGbHclM0QlM0Q; _ym_visorc=b; dfp_group=35; _dc_gtm_UA-2546784-1=1'

}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'avito_parse.middlewares.AvitoParseSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'avito_parse.middlewares.AvitoParseDownloaderMiddleware': 543,
    "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
    "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
    'avito_parse.middlewares.TooManyRequestsRetryMiddleware': 543,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None
}
DOWNLOADER_CLIENT_TLS_METHOD = "TLSv1.2"


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

IMAGE_STORE = 'images'

ITEM_PIPELINES = {
    "avito_parse.pipelines.GbParsePipeline": 100,
    "avito_parse.pipelines.GbParseMongoPipeline": 200,
    "avito_parse.pipelines.GbImageDownloadPipeline": 50,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True
# AUTOTHROTTLE_ENABLED = True
# # The initial download delay
# AUTOTHROTTLE_START_DELAY = 3
# # The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 10
# # The average number of requests Scrapy should be sending in parallel to
# # each remote server
# # AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# # Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# ROTATING_PROXY_LIST_PATH = (
#     "/Users/Kate/Python/Data Mining/Lesson1/proxies"
# )

RETRY_HTTP_CODES = [429]
