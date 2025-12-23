from django import forms

#发布博客表单，有标题、内容和分类信息
class PubBlogForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=2)
    content = forms.CharField(min_length=2)
    category = forms.IntegerField()