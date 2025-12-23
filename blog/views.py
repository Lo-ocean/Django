from django.http import JsonResponse
from django.shortcuts import render,redirect,reverse
from django.contrib.auth.decorators import  login_required
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods,require_POST,require_GET
from .forms import PubBlogForm
from .models import BlogComment, Blog, BlogCategory
from django.db.models import Q
# Create your views here.

#首页
def index(request):
    blogs = Blog.objects.all()
    return render(request, 'index.html', context={"blogs":blogs})

#博客详情
def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk = blog_id)
    except Exception as e:
        blog = None
    return render(request, 'blog_detail.html', context={"blog": blog})

#发布博客   要求：用户登录后可发布
@require_http_methods(['GET','POST'])
@login_required(login_url=reverse_lazy("user_auth:login"))
def pub_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request,'pub_blog.html', context={"categories": categories})
    else:
        #获取提交的表单
        form  = PubBlogForm(request.POST)
        #判断是否正确
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            #正确添加数据到数据库中，返回对应的json数据
            blog = Blog.objects.create(title=title, content=content, category_id=category_id,author=request.user)
            return JsonResponse({"code": 200, "message": "博客发布成功", "data": {"blog_id": blog.id}})
        else:
            #错误打印对应的错误信息，返回对应的json数据
            print(form.errors)
            return JsonResponse({"code": 400, "message": "参数错误"})


# 评论    要求：用户登录后可评论
@require_POST
@login_required(login_url=reverse_lazy("user_auth:login"))
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(content=content, blog_id=blog_id,author=request.user)
    #重新加载博客详情页
    return redirect(reverse("blog:blog_detail", kwargs={"blog_id": blog_id}))

#搜索
@require_GET
def search(request):
    #/search/?q=***
    q = request.GET.get('q')
    blogs = Blog.objects.filter(Q(title__icontains=q)|Q(content__icontains=q)).all()
    return render(request, 'index.html', context={"blogs":blogs})
