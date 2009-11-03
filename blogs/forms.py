# coding=UTF-8
from django import forms

class BlogForm(forms.Form):
    title=forms.CharField(label='主题',max_length=50,required=True)
    category=forms.ChoiceField(label='分类',required=False)
    user_tag=forms.CharField(label='自定义分类',max_length=10,required=False)
    content=forms.CharField(label='内容',widget=forms.Textarea,required=True)

class CommentForm(forms.Form):
    content=forms.CharField(label='发表评论',widget=forms.Textarea,required=True)

class URLForm(forms.Form):
    name=forms.CharField(label='链接名称',required=True)
    URL=forms.URLField(label='链接地址',required=True)

class ConfigurationForm(forms.Form):
    title=forms.CharField(label='博客标题',required=True)
    motto=forms.CharField(label='座右铭',required=True)
