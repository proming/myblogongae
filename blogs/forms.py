# coding=UTF-8
from django import forms

class BlogForm(forms.Form):
    title=forms.CharField(label='主题',
                widget=forms.TextInput(attrs={'size':'40'}),
                max_length=50,required=True,
                error_messages={'required': u'请输入标题'})
    category=forms.ChoiceField(label='分类',required=False)
    user_tag=forms.CharField(label='自定义分类',max_length=10,required=False)
    content=forms.CharField(label='内容',widget=forms.Textarea,required=True)

class CommentForm(forms.Form):
    author=forms.CharField(label='昵称',
                widget=forms.TextInput(attrs={'size':'40'}),
                max_length=20, required=True, 
                error_messages={'required': u'请输入您的昵称'})
    email=forms.EmailField(label='邮箱',
                widget=forms.TextInput(attrs={'size':'40'}),
                required=True,
                error_messages={'required': u'请输入您的邮箱'})
    content=forms.CharField(label='发表评论',widget=forms.Textarea,required=True,
                error_messages={'required': u'请输入您的留言'})

class URLForm(forms.Form):
    name=forms.CharField(label='链接名称',
              widget=forms.TextInput(attrs={'size':'40'}),
              required=True,
                error_messages={'required': u'请输入链接名称'})
    URL=forms.URLField(label='链接地址',
              widget=forms.TextInput(attrs={'size':'40'}),
              required=True,
              error_messages={'required': u'请输入链接地址'})

class ConfigurationForm(forms.Form):
    title=forms.CharField(label='博客标题',
                widget=forms.TextInput(attrs={'size':'40'}), 
                error_messages={'required': u'请输入您的博客标题'},
                required=True)
    motto=forms.CharField(label='座右铭',
                widget=forms.TextInput(attrs={'size':'40'}), 
                error_messages={'required': u'请输入您的座右铭'},
                required=True)
    pagesize=forms.IntegerField(label='页面日志数',min_value=3, 
                error_messages={'required': u'最小值为3'},
                required=True)


