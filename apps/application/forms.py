from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.forms import ModelForm, ModelChoiceField
from .models import Application
from assets.models import Assets ,Platform
from django import forms


class ApplicationCreateForm(ModelForm):

    # overwirte __init_ 为前台表单显示主表数据platform_name值，Platform model 必须定义__str__()  返回platform_name
    def __init__(self, *args, **kwargs):
        super(ApplicationCreateForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['platform'] = ModelChoiceField(queryset=Platform.objects.all(), empty_label=None, label="项目平台")


    class Meta:
        model = Application
        fields = ['items',  'platform', 'env', 'ipaddress', 'package_name', 'dst_path', 'backup_path']
        help_texts = {
            # 'package_name': ('包名'),
            #
        }

class ApplicationUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ApplicationUpdateForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            #self.fields['platform'] = ModelChoiceField(queryset=Platform.objects.all(), empty_label=None, label="项目平台")
            self.fields['ipaddress'] = ModelChoiceField(queryset=Assets.objects.all(), empty_label=None, label="解析地址")

    class Meta:
        model = Application
        fields = [
            'items', 'platform', 'env',
        ]
