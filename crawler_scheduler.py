import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from crawler.crawler import Crawler

def start_crawling():
    print(f"Start crawling PTT Stock at {datetime.datetime.today()}.")
    crawler = Crawler()
    crawler.crawl()

def main():
    scheduler = BackgroundScheduler(timezone="Asia/Taipei")
    scheduler.add_job(
        id="crawl_ptt_stock_celebrity_pushes",
        func=start_crawling,
        trigger="interval",
        hours=0.5,
        start_date=datetime.datetime.now(),
        next_run_time=datetime.datetime.now()
    )
    scheduler.start()


if __name__ == "__main__":
    main()
    while True:
        time.sleep(600)
