from apscheduler.triggers.cron import CronTrigger
from django.http import JsonResponse
from django.views.generic import View

from apps.tasks.scrapyd.tasks import *


class ListTaskApi(View):

    @classmethod
    def post(cls, request, *args, **kwargs):
        job_list = JobInfo.objects.all()
        data = []
        for job in job_list:
            data.append({
                'job_id': job.job_id,
                'job_name': job.job_name,
                'job_status': job.job_status,
                'job_cron': job.job_cron,
                'job_func': job.job_func,
                'job_args': job.job_args,
                'job_kwargs': job.job_kwargs,
                'job_trigger': job.job_trigger,
                'job_next_run_time': job.job_next_run_time,
                'job_success_count': job.job_success_count,
                'job_fail_count': job.job_fail_count,
                'job_start_time': job.job_start_time,
                'job_end_time': job.job_end_time,
                'job_create_time': job.job_create_time,
                'job_update_time': job.job_update_time,
            })
        return JsonResponse({'code': 200, 'msg': '查询成功', 'data': data})


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
        if not all([job_name, job_cron, job_func]):
            return JsonResponse({'code': 400, 'msg': '参数错误'})
        if job_args is None:
            job_args = '[]'
        if job_kwargs is None:
            job_kwargs = '{}'
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


class ModifyTaskStatusStopApi(View):
    """
    暂停任务接口
    """

    @classmethod
    def post(cls, request, *args, **kwargs):
        job_name = request.POST.get('job_name')
        job_info = JobInfo.objects.get(job_name=job_name)
        scheduler.pause_job(job_info.job_id)
        job_info.job_status = 'stop'
        job_info.save()
        return JsonResponse({'code': 200, 'msg': '暂停成功'})


class ModifyTaskStatusStartApi(View):
    """
    启动任务接口
    """

    @classmethod
    def post(cls, request, *args, **kwargs):
        job_name = request.POST.get('job_name')
        job_info = JobInfo.objects.get(job_name=job_name)
        scheduler.resume_job(job_info.job_id)
        job_info.job_status = 'running'
        job_info.save()

        return JsonResponse({'code': 200, 'msg': '启动成功'})


class ModifyTaskStatusInfoApi(View):
    """
    修改任务详情接口
    """

    @classmethod
    def post(cls, request, *args, **kwargs):
        job_name = request.POST.get('job_name')
        job_info = JobInfo.objects.get(job_name=job_name)
        job_cron = request.POST.get('job_cron')
        job_func = request.POST.get('job_func')
        job_args = request.POST.get('job_args')
        job_kwargs = request.POST.get('job_kwargs')
        if not all([job_name, job_cron, job_func]):
            return JsonResponse({'code': 400, 'msg': '参数错误'})
        if job_args is None:
            job_args = '[]'
        if job_kwargs is None:
            job_kwargs = '{}'
        job_args = eval(job_args) if job_args else []
        job_kwargs = eval(job_kwargs) if job_kwargs else {}
        job_func = eval(job_func)
        job_kwargs['job_name'] = job_name
        job_cron_list = job_cron.split(' ')
        trigger = CronTrigger(second=job_cron_list[0], minute=job_cron_list[1], hour=job_cron_list[2], day=job_cron_list[3], month=job_cron_list[4], day_of_week=job_cron_list[5])
        job = scheduler.modify_job(job_info.job_id, func=job_func, trigger=trigger, args=job_args, kwargs=job_kwargs, max_instances=10)
        job_info.job_cron = job_cron
        job_info.job_func = job_func
        job_info.job_args = job_args
        job_info.job_kwargs = job_kwargs
        job_info.job_next_run_time = job.next_run_time
        job_info.save()
        return JsonResponse({'code': 200, 'msg': '修改成功'})
