from django.db import models


class JobInfo(models.Model):
    job_id = models.CharField(max_length=64, verbose_name='任务ID')
    job_name = models.CharField(max_length=64, verbose_name='任务名称')
    job_status = models.CharField(max_length=64, verbose_name='任务状态')
    job_cron = models.CharField(max_length=64, verbose_name='任务cron')
    job_func = models.CharField(max_length=64, verbose_name='任务函数')
    job_args = models.CharField(max_length=64, verbose_name='任务参数')
    job_kwargs = models.CharField(max_length=64, verbose_name='任务kwargs')
    job_instance = models.CharField(max_length=64, verbose_name='任务实例')
    job_trigger = models.CharField(max_length=64, verbose_name='任务触发器')
    job_next_run_time = models.CharField(max_length=64, verbose_name='下次运行时间')
    job_success_count = models.IntegerField(verbose_name='成功次数')
    job_fail_count = models.IntegerField(verbose_name='失败次数')
    job_start_time = models.CharField(max_length=64, verbose_name='开始时间')
    job_end_time = models.CharField(max_length=64, verbose_name='结束时间')
    job_create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    job_update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = "job_info"
        verbose_name = '任务信息'
        verbose_name_plural = verbose_name
