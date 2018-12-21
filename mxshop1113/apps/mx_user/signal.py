# coding=utf-8
from mx_user.models import UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=UserProfile)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
        #密码加密
        instance.set_password(instance.password)
        #保存
        instance.save()