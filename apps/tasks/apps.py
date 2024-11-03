from django.apps import AppConfig


class TaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tasks'

    def ready(self):
        # 不能在外部提前导入，否则会导致django未加载完成
        from apps.tasks.jobs import scheduler
        scheduler.start()
