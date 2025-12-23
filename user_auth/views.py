import string
import random
from django.shortcuts import render,redirect,reverse
from django.http.response import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.http import  require_http_methods
from user_auth.models import CaptchaModel
from .forms import RegisterForm,LoginForm
from django.contrib.auth import get_user_model,login,logout


User = get_user_model()


# Create your views here.
@require_http_methods(['GET','POST'])
def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            #获取表单信息
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email = email).first()
            #验证表单信息
            if user and user.check_password(password):
                #True:登录
                login(request,user)
                #是否点击记住我
                if not remember:
                    #是否点击记住我，点击不进行操作，不点击设置过期时间为0
                    request.session.set_expiry(0)
                return redirect('/')
            else:
                print('邮箱或密码错误！')
                #添加错误信息到表单
                form.add_error('email','邮箱或密码错误！')
                return render(request, 'login.html',context={"form": form})
                #另一种回退到登录页面的方式
                #return redirect(reverse('user_auth:login'))
        else:
            #表单验证失败时返回登录页面
            return render(request,'login.html',context={'form':form})



@require_http_methods(['GET', 'POST' ])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            #获取表单，注册用户
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse('user_auth:login'))
        else:
            print(form.errors)
            #重新跳转到注册页面
            #return redirect(reverse('user_auth:register'))

            return render(request,'register.html', context={"form": form})

def user_logout(request):
    #退出
    logout(request)
    return redirect('/')


def send_captcha(request):
    email = request.GET.get('email')
    #判空
    if not email:
        return JsonResponse({"code": 400, "message": '邮箱不能为空'})
    #将发送的邮箱验证码添加到数据库中，并在窗口显示'邮箱验证码发送成功！'信息
    captcha = "".join(random.sample(string.digits, 4))
    CaptchaModel.objects.update_or_create(email = email,defaults = {'captcha': captcha})
    send_mail("博客注册验证", message = f"您的注册验证码是：{captcha}", recipient_list = [email], from_email = None)
    return JsonResponse({"code": 200, "message": "邮箱验证码发送成功！"})
