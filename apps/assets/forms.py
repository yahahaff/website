from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.forms import ModelForm, ModelChoiceField
from .models import Assets, Platform
from django import forms


class UserUpdateForm(ModelForm):
    username = forms.CharField(
        required=True,
        label="用户名",
        widget=forms.TextInput(
            attrs={'class': 'special'},
        )
    )
    password = forms.CharField(
        required=False, label="密码",
        max_length=32, strip=False,
        widget=forms.PasswordInput,
    )

    last_name = forms.CharField(
        required=True, label="名称",
        widget=forms.TextInput(
            attrs={'class': 'special'},
        )
    )
    is_superuser = forms.ChoiceField(
        required=False, label="用户角色",
        choices=((True, '管理员'), (False, '用户'),),
    )
    email = forms.EmailField(
        required=False, label="邮箱",
        widget=forms.EmailInput(
            attrs={'class': 'special'},
        )
    )
    is_active = forms.ChoiceField(
        required=False, label="用户状态",
        choices=((True, '激活'), (False, '封停'),),

    )

    class Meta:
        model = Assets
        fields = ['username', 'password', 'last_name', 'email', 'is_superuser', 'is_active']
        error_messages = {
            'username': {'max_length': "名字长度应在15个字符以内"},
        }




class AssetCreateForm(ModelForm):
    # overwirte __init_ 为前台表单显示主表数据platform_name值，Platform model 必须定义__str__()  返回platform_name
    def __init__(self, *args, **kwargs):
        super(AssetCreateForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['project'] = ModelChoiceField(queryset=Platform.objects.all(), empty_label=None, label="项目平台")

    class Meta:
        model = Assets
        fields = [
            'hostname', 'ip', 'port', 'localtion', 'vendor',
            'login_user', 'model', 'platform', 'project', 'comment',

        ]
        widgets = {
            'login_user': forms.TextInput(),
            'port': forms.TextInput(),

        }

        help_texts = {
            'platform': ("Windows 2016 RDP protocol is different, If is window 2016, set it"),

        }
class AssetUpdateForm(ModelForm):
    class Meta:
        model = Assets
        fields = [
            'hostname', 'ip', 'port', 'localtion', 'vendor',
            'login_user', 'model', 'platform', 'comment',


        ]
        widgets = {
            'login_user': forms.TextInput(),
            'port': forms.TextInput(),

        }
        help_texts = {
            'platform': ("Windows 2016 RDP protocol is different, If is window 2016, set it"),

        }