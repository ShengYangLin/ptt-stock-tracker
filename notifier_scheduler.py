import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from backend.line_notification import send_message

def start_notify():
    print(f"Start Notifying at {datetime.datetime.today()}.")
    send_message()

def main():
    scheduler = BackgroundScheduler(timezone="Asia/Taipei")
    scheduler.add_job(
        id="send_ptt_stock_celebrity_pushes",
        func=start_notify,
        trigger="interval",
        hours =0.5,
        start_date=datetime.datetime.now(),
        next_run_time=datetime.datetime.now()
    )
    scheduler.start()


if __name__ == "__main__":
    main()
    while True:
        time.sleep(600)