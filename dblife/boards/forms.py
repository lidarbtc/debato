from django import forms
from .models import Comment
class BoardForm(forms.Form):
    title = forms.CharField(
        error_messages={
            'required': '제목을 입력해주세요.'
        }, max_length=64, label="제목")
    contents = forms.CharField(
        error_messages={
            'required': '내용을 입력해주세요.'
        },widget=forms.Textarea, label = "내용")
    tags = forms.CharField(required=False, label = "태그")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']