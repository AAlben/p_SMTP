from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

from sent_email import send

if __name__ == '__main__':
    send()
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 20},
        'processpool': ProcessPoolExecutor(max_workers=5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    sched = BlockingScheduler()
    sched.configure(executors=executors, job_defaults=job_defaults)
    sched.add_job(send, 'cron', hour=7, minute=30, misfire_grace_time=200)
    sched.add_job(send, 'cron', hour=9, minute=10, misfire_grace_time=200)
    sched.add_job(send, 'cron', hour=13, minute=0, misfire_grace_time=200)
    sched.add_job(send, 'cron', hour=19, minute=0, misfire_grace_time=200)
    sched.start()
