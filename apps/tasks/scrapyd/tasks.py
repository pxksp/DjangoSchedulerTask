import random
import time

from apps.tasks.jobs import scheduler
from apps.tasks.models import JobInfo


def run_scrapy(*args, **kwargs):
    job_name = kwargs.get('job_name')
    job_info = JobInfo.objects.get(job_name=job_name)
    if job_info.job_status == 'stop':
        return False
    job_id = job_info.job_id
    job = scheduler.get_job(job_id)
    job_info.job_next_run_time = job.next_run_time
    job_info.job_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    job_info.job_status = 'running'
    job_info.save()
    try:
        time.sleep(random.randint(1, 5))
        print('scrapy run success')
        job_info.job_success_count += 1
        job_info.job_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        job_info.job_status = 'success'
        job_info.save()
        return True
    except Exception as e:
        job_info.job_fail_count += 1
        job_info.job_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        job_info.job_status = 'fail'
        job_info.save()
        return False