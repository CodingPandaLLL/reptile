"""mysites URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from reptile import views
from django.views.static import serve  # 导入静态文件模块
from django.conf import settings  # 导入配置文件里的文件上传配置

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # path('hello/', views.hello, name='hello'),
    path('article-<int:aid>.html/', views.article, name='article'),
    path('image-<int:iid>.html/', views.image, name='image'),
    path('ra/', views.reptileArticle, name='reptileArticle'),
    path('ri/', views.reptileImage, name='reptileImage'),
    path('rv/', views.reptileVideo, name='reptileVideo'),
    path('video-<int:vid>.html/', views.video, name='video'),
    path('ueditor/', include('DjangoUeditor.urls')),  # 添加DjangoUeditor的URL
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # 增加此行
]
