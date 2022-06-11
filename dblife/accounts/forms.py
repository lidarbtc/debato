from django import forms
from .models import User
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    useremail = forms.EmailField(
        error_messages={
            'required': '아이디를 입력해주세요.'
        }, max_length=64, label="사용자 이메일")
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },widget=forms.PasswordInput, label = "비밀번호")

    def clean(self):
        cleaned_data = super().clean()
        useremail = cleaned_data.get('useremail')
        password = cleaned_data.get('password')

        if useremail and password:
            user = User.objects.get(useremail=useremail)
            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀립니다.')
            else:
                self.user_id = user.id
            