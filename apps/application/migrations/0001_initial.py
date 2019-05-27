# Generated by Django 2.1 on 2019-05-27 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.CharField(help_text='项目名称，如sobet，lottery，admin', max_length=100, verbose_name='应用')),
                ('port', models.CharField(default=8080, max_length=10, verbose_name='端口')),
                ('env', models.CharField(default='', help_text='项目名称，DEV，TK', max_length=10, verbose_name='环境')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('package_name', models.CharField(default='', help_text='合法包名，允许字段为空', max_length=100, verbose_name='包名')),
                ('type', models.IntegerField(default='0', help_text='0 静态 1 全量war包 2 增量包 3 Jar包', verbose_name='发布类型')),
                ('dst_path', models.CharField(default='', help_text='文件发布路径', max_length=200, verbose_name='发布路径')),
                ('backup_path', models.CharField(default='', help_text='备份根目录', max_length=200, verbose_name='备份地址')),
                ('configs', models.CharField(default='', help_text='项目配置文件信息', max_length=3000, verbose_name='配置文件')),
                ('runuser', models.CharField(default='root', help_text='文件属主或启动用户', max_length=100, verbose_name='属主')),
                ('update_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='更新时间')),
                ('comment', models.TextField(blank=True, default='', max_length=128, verbose_name='备注')),
                ('ipaddress', models.ForeignKey(default='1', help_text='服务器IP地址', on_delete=django.db.models.deletion.CASCADE, to='assets.Assets', verbose_name='服务器地址ID')),
                ('platform', models.ForeignKey(default='', help_text='平台名称', on_delete=django.db.models.deletion.CASCADE, to='assets.Platform', verbose_name='平台代码')),
            ],
        ),
    ]
