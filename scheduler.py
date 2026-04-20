# python scheduler.py & forget. Runs forever, every 15min. 🕐 Or cron if you want.
import schedule
import time
from main import main

schedule.every(15).minutes.do(main)
# schedule.every().hour.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
