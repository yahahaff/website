from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.forms import ModelForm, ModelChoiceField
from .models import Domains
from django import forms
from assets.models import Assets , Platform


class DomainCreateForm(ModelForm):

    # overwirte __init_ 为前台表单显示主表数据platform_name值，Platform model 必须定义__str__()  返回platform_name
    def __init__(self, *args, **kwargs):
        super(DomainCreateForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['platform'] = ModelChoiceField(queryset=Platform.objects.all(), empty_label=None, label="项目平台")


    class Meta:
        model = Domains
        fields = [
            'domain', 'platform', 'filing', 'is_encryption', 'start_time',
            'expire_time', 'is_active',
        ]
        widgets = {
            'domain': forms.TextInput(),
            'start_time': forms.DateInput,
            'expire_time': forms.DateInput,
        }

        help_texts = {
            'platform': ("Windows 2016 RDP protocol is different, If is window 2016, set it"),

        }
class DomainUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(DomainUpdateForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['platform'] = ModelChoiceField(queryset=Platform.objects.all(), empty_label=None, label="项目平台")
            self.fields['resolve'] = ModelChoiceField(queryset=Assets.objects.all(), empty_label=None, label="解析地址")

    class Meta:
        model = Domains
        fields = [
            'domain', 'platform', 'resolve', 'filing', 'start_time', 'is_encryption',
            'expire_time', 'ssl_begin', 'ssl_expire', 'ssl_issuer', 'is_active'
        ]
        # widgets = {
        #
        #     'login_user': forms.TextInput(),
        #     'port': forms.IntegerField(),
        #
        # }
        help_texts = {

        }