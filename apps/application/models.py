from django.db import models
from assets.models import Assets ,Platform
# Create your models here.
from django.db import models

# Create your models here.

class Application(models.Model):
    ENV_CHOICE = (('DEV', '开发环境'), ('TK', '测试环境'), ('PRE', '预发布环境'), ('Online', '线上环境'))

    items = models.CharField(max_length=100, verbose_name=('应用'))
    port = models.CharField(max_length=10,  default=8080, verbose_name=('端口'))
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, default='', verbose_name=('平台代码'),)
    env = models.CharField(max_length=10, choices=ENV_CHOICE,verbose_name=('环境'), default='',)
    status = models.BooleanField(default=True, verbose_name=('状态'))
    package_name = models.CharField(max_length=100, default='', verbose_name=('包名'))
    type = models.IntegerField(default='0', verbose_name=('发布类型'), help_text='0 静态 1 全量war包 2 增量包 3 Jar包')
    dst_path = models.CharField(max_length=200, default='', verbose_name=('发布路径'),  help_text='文件发布路径')
    backup_path = models.CharField(max_length=200, default='', verbose_name=('备份地址'), help_text='备份根目录')
    ipaddress = models.ForeignKey(Assets, on_delete=models.CASCADE, default='1', verbose_name=('服务器地址ID'),
                                  help_text='服务器IP地址')
    configs = models.CharField(max_length=3000, default='', verbose_name=('配置文件'), help_text='项目配置文件信息')
    runuser = models.CharField(max_length=100, default='root', verbose_name=('属主'), help_text='文件属主或启动用户')
    update_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=('更新时间'))
    comment = models.TextField(max_length=128, default='', blank=True, verbose_name=('备注'))


class App_history(models.Model):
    items = models.CharField(max_length=100)
    platform = models.CharField(max_length=20, default='')
    env = models.CharField(max_length=10,  verbose_name=('环境'), default='', )
    status = models.BooleanField(default=True, verbose_name=('状态'))
    type = models.IntegerField(default='0', verbose_name=('发布类型'), help_text='0 静态 1 全量war包 2 增量包 3 Jar包')
    app_dir = models.CharField(max_length=200, default='', verbose_name=('发布路径'), help_text='文件发布路径')
    backup = models.CharField(max_length=200, default='', verbose_name=('备份地址'), help_text='备份文件')
    ipaddress = models.CharField(max_length=20, default='1', verbose_name=('服务器地址ID'),help_text='服务器IP地址')
    opsuser = models.CharField(max_length=100, default='root', verbose_name=('属主'), help_text='文件属主或启动用户')
    update_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=('更新时间'))