from django.db import models

# Create your models here.
#
class Platform(models.Model):
    platform_name = models.CharField(max_length=64, unique=True, default='',
                                     verbose_name=('Platform_name'), help_text="项目平台")

    def __str__(self):
        return self.platform_name


class Assets(models.Model):
    PLATFORM_CHOICES = (
        ('Linux', 'Linux'),
        ('Windows', 'Windows'),
        ('BSD', 'BSD'),
        ('Other', 'Other'),
    )
    #General
    ip = models.GenericIPAddressField(max_length=32, verbose_name=('IP'), db_index=True, unique=True)
    hostname = models.CharField(max_length=128, verbose_name=('Hostname'))
    port = models.IntegerField(default=22, verbose_name=('Port'))
    platform = models.CharField(max_length=128, choices=PLATFORM_CHOICES, default='Linux', verbose_name=('系统平台'))
    project = models.ForeignKey(Platform, on_delete=False, help_text="项目平台", verbose_name=('项目平台'))
    is_active = models.BooleanField(default=True, verbose_name=('Is active'))
    # Auth
    login_user = models.CharField(max_length=32, null=False, blank=True, default='root', verbose_name=('管理用户'))
    # Collect
    vendor = models.CharField(max_length=64, null=True, blank=True, verbose_name=('厂商'))
    localtion = models.CharField(max_length=64, null=True, blank=True, verbose_name=('区域'))
    model = models.CharField(max_length=54, null=True, blank=True, verbose_name=('Model'))
    cpu_model = models.CharField(max_length=64, null=True, blank=True, verbose_name=('CPU model'))
    cpu_cores = models.IntegerField(null=True, verbose_name=('CPU cores'))
    memory = models.CharField(max_length=64, null=True, blank=True, verbose_name=('Memory'))
    disk_total = models.CharField(max_length=1024, null=True, blank=True, verbose_name=('Disk total'))
    asset_number = models.CharField(max_length=32, null=True, blank=True, verbose_name=('Asset number'))
    #os
    os = models.CharField(max_length=128, null=True, blank=True, verbose_name=('OS'))
    os_version = models.CharField(max_length=16, null=True, blank=True, verbose_name=('OS version'))
    created_by = models.CharField(max_length=32, null=True, blank=True, verbose_name=('Created by'))
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=('Date created'))
    comment = models.TextField(max_length=128, default='', blank=True, verbose_name=('备注'))


