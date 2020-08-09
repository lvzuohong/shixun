import time
from apscheduler.schedulers.blocking import BlockingScheduler
import longhubang


sched =BlockingScheduler()

@sched.scheduled_job('interval',minutes=5)
def my_job():
  longhubang.paquzhixing()
sched.start()