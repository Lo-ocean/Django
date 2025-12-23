#  Django Blog web

### 项目简介

本项目为基于Python3.10+和Django5.2构建的博客网站。它不仅提供传统博客的所有的核心功能，还能通过bootstrap5和来定制您的网站。
页面较为简洁但可定制性高，所需的文件放在static目录下了可通过阅读以下链接内容来定制自己的博客网站：

定制网页页面： https://getbootstrap.com/ 
定制代码高亮： https://highlightjs.org/ 


### **网站详情：**

    全文搜索：当用户搜索博客时会搜索标题或内容相符的博客返回。
    注册：会根据用户名、邮箱、邮箱验证码和密码进行注册。
    登录后：主页面的登录、注册按钮会替换成用户头像(可点击会显示下拉框退出登录)。
    发布博客：必须登录后才可发布博客，内容部分带有highlight的代码高亮样式。
    博客详情：必须登录后才可评论。
    
### 快速开始：

##### 1.环境准备：
确保您的系统中已安装Python3.10+、Django5.2和MySQL。

##### 2.克隆
    # 克隆项目到本地
    git clone https://github.com/Lo-ocean/Django.git

##### 3. 项目配置
数据库配置：打开first_project的settings.py文件，找到 DATABASES 配置项，修改为您的 MySQL 连接信息。
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'djangoblog',
            'USER': 'root',
            'PASSWORD': 'your_password',
            'HOST': '127.0.0.1',
            'PORT': 3306,
        }
    }

##### 4. 初始化数据库
    python manage.py makemigrations
    python manage.py migrate

    # 创建一个超级管理员账户
    python manage.py createsuperuser
