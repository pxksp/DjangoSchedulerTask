from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler

# 调用start后主线程不会阻塞。当你不运行任何其他框架时使用，并希望调度器在你应用的后台执行。
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')
