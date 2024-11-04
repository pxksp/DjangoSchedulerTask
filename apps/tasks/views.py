import random
import time

from apscheduler.triggers.cron import CronTrigger
from django.http import JsonResponse
from django.views.generic import View

from apps.tasks.jobs import scheduler
from apps.tasks.models import JobInfo





class AddTaskApi(View):
    """
    添加任务接口
    """

    @classmethod
    def post(cls, request, *args, **kwargs):
        job_name = request.POST.get('job_name')
        job_cron = request.POST.get('job_cron')
        job_func = request.POST.get('job_func')
        job_args = request.POST.get('job_args')
        job_kwargs = request.POST.get('job_kwargs')
        if not all([job_name, job_cron, job_func, job_args, job_kwargs]):
            return JsonResponse({'code': 400, 'msg': '参数错误'})
        if JobInfo.objects.filter(job_name=job_name).exists():
            return JsonResponse({'code': 400, 'msg': '任务已存在'})
        job_args = eval(job_args) if job_args else []
        job_kwargs = eval(job_kwargs) if job_kwargs else {}
        job_func = eval(job_func)
        job_status = 'init'
        job_kwargs['job_name'] = job_name
        job_cron_list = job_cron.split(' ')
        trigger = CronTrigger(second=job_cron_list[0], minute=job_cron_list[1], hour=job_cron_list[2], day=job_cron_list[3], month=job_cron_list[4], day_of_week=job_cron_list[5])
        job = scheduler.add_job(job_func, trigger, args=job_args, kwargs=job_kwargs, max_instances=10)
        job_id = job.id
        JobInfo.objects.create(
            job_id=job_id,
            job_name=job_name,
            job_status=job_status,
            job_cron=job_cron,
            job_func=job_func,
            job_args=job_args,
            job_kwargs=job_kwargs,
            job_next_run_time=job.next_run_time
        )
        return JsonResponse({'code': 200, 'msg': '添加成功'})
