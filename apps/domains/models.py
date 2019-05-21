from django.db import models
from assets.models import Platform, Assets

YES_NO_CHOICE = ((True, '是'), (False, '否'),)


# Create your models here.
class Domains(models.Model):
    domain = models.CharField(max_length=100, db_index=True, unique=True, null=False, blank=False,)
    platform = models.ForeignKey(Platform, on_delete=False, verbose_name=('项目'), related_name='platformS')
    resolve = models.ForeignKey(Assets, on_delete=False, null=True, help_text="域名解析地址", related_name='resolveS')
    filing = models.BooleanField(default=False, choices=YES_NO_CHOICE, verbose_name=('是否备案'))
    start_time = models.DateField(null=True, blank=True, verbose_name=('采购时间'))
    expire_time = models.DateField(null=True, blank=True, verbose_name=('到期时间'))
    is_encryption = models.BooleanField(default=True, verbose_name=('是否HTTPS'), choices=YES_NO_CHOICE)
    ssl_begin = models.DateField(null=True, blank=True, verbose_name=('SSL到期时间'))
    ssl_expire = models.DateField(null=True, blank=True, verbose_name=('SSL 到期时间'))
    ssl_issuer = models.CharField(max_length=64, null=True, blank=True, verbose_name=('SSL证书品牌'))
    remainder_days = models.IntegerField(null=True, help_text="证书剩余天数")
    is_active = models.BooleanField(default=True, verbose_name=('状态'), choices=YES_NO_CHOICE)
    vendor = models.CharField(max_length=64, null=True, blank=True, verbose_name=('厂商'))
    created_by = models.CharField(max_length=32, null=True, blank=True, verbose_name=('Created by'))
    update_time = models.DateTimeField(auto_now=True, null=True, help_text="更新时间")
    comment = models.TextField(max_length=128, default='', null=True, blank=True, verbose_name=('Comment'))

    def __str__(self):
        return self.domain
