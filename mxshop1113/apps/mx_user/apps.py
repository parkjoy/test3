from django.apps import AppConfig


class MxUserConfig(AppConfig):
    name = 'mx_user'
    verbose_name = "用户表"

    # def ready(self):
    #     import mx_user.signal

