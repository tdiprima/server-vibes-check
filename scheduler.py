# python scheduler.py & forget. Runs forever, every 15min. 🕐 Or cron if you want.
import schedule
import time
from main import main  # Assuming main.py has main()

schedule.every(15).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
