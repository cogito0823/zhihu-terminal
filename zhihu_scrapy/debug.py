from scrapy import cmdline


name = 'answer'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
