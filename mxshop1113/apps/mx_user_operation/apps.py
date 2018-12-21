from django.apps import AppConfig


class MxUserOperationConfig(AppConfig):
    name = 'mx_user_operation'
    verbose_name = "用户操作表"

    def ready(self):
        import mx_user_operation.signal