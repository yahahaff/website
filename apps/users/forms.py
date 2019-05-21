from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.forms import ModelForm
from django.contrib.auth.models import User
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
        model = User
        fields = ['username', 'password', 'last_name', 'email', 'is_superuser', 'is_active']
        error_messages = {
            'username': {'max_length': "名字长度应在15个字符以内"},
        }




class UserCreateForm(ModelForm):
    username = forms.CharField(
        required=True,
        label="用户名",
        widget=forms.TextInput(
            attrs={'class': 'special'},
        )
    )
    password = forms.CharField(
        required=True, label="密码",
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
        required=False, label="用户角色", initial=False,
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
        model = User
        fields = ['username', 'password', 'last_name', 'email', 'is_superuser', 'is_active']

        error_messages = {
            'username': {'max_length': "名字长度应在15个字符以内", },
        }
