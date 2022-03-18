# Citation for the file:
# Date: 3/12/2022
# Modified from:
# Source URL: https://stackoverflow.com/questions/41495052/scrapy-reactor-not-restartable

# this file forks a separate process to run the web scraping spider multiple times

from multiprocessing import Queue, Process
from scrapy import crawler
from twisted.internet import reactor

test = []
qt = ""

def new_process_spider(output_queue, spider, query_text):
    """Runs a new spider process which invokes the crawler to web scrape for data."""
    global qt
    try:
        qt = query_text
        runner = crawler.CrawlerRunner()
        deferred = runner.crawl(spider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        output_queue.put(test[0])
    except Exception as e:
        output_queue.put(e)


def run_spider(spider, query_text, spider_thread):
    """Create a new process and wait for results from the newly created process. The results are put into a variable
    q2."""
    global test
    output_queue = Queue()
    p = Process(target=new_process_spider, args=(output_queue, spider, query_text))
    p.start()
    result = output_queue.get()
    p.join()
    #test.append(result[0])
    spider_thread.result = result


