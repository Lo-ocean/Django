from django.urls import path
from . import views

app_name = 'user_auth'

urlpatterns = [
    path('login', views.user_login, name='login'),

    path('logout',views.user_logout, name='logout'),

    path('register', views.register, name='register'),

    path('email_captcha', views.send_captcha, name='email_captcha')
]