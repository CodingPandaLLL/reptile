from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import time
import os
import shutil

from django.http import HttpResponse
# 比如我信要查询所有文章，我们就要views.py文件头部把文章表从数据模型导入
from .models import Article, Image, Video


# def index(request):
#     all_images = Image.objects.all()  # 通过Image表查出所有
#     # 把查询出来的分类封装到上下文里
#     context = {
#         'allcategory': all_images,
#     }
#     return render(request, 'index.html', context)  # 把上下文传到index.html页面


def index(request):
    # 添加两个变量，并给它们赋值
    sitename = 'Django中文网'
    url = 'www.django.cn'
    # 新加一个列表
    list = [
        '开发前的准备',
        '项目需求分析',
        '数据库设计分析',
        '创建项目',
        '基础配置',
        '欢迎页面',
        '创建数据库模型',
    ]
    # 对Article进行声明并实例化，然后生成对象allarticle
    video_list = Video.objects.all()
    article_list = Article.objects.all()
    image_list = Image.objects.all()
    # 把两个变量封装到上下文里
    context = {
        'sitename': sitename,
        'url': url,
        'list': list,  # 把list封装到context
        'videoList': video_list,
        'articleList': article_list,
        'imageList': image_list,
    }
    # 把上下文传递到模板里
    return render(request, 'index.html', context)


def video(request, vid):
    # 对video进行声明并实例化，然后生成对象videoContent
    videoContent = Video.objects.get(id=vid)

    # 把两个变量封装到上下文里
    context = {
        'videoContent': videoContent,
    }
    # 把上下文传递到模板里
    return render(request, 'video.html', context)


def article(request, aid):
    print('测试打印', aid)
    # 对Article进行声明并实例化，然后生成对象articleContent
    articleContent = Article.objects.get(id=aid)
    # 把两个变量封装到上下文里
    context = {
        'articleContent': articleContent,
    }
    # 把上下文传递到模板里
    return render(request, 'article.html', context)


def image(request, iid):
    # 对image进行声明并实例化，然后生成对象imageContent
    imageContent = Image.objects.get(id=iid)
    image_path = imageContent.image_path
    # 处理图片地址，改为可读取的图片地址
    new_path = ''
    imageResult = []
    pathArr = image_path.split(',')
    for ipath in pathArr:
        imageResult.append('/static/imgs/' + ipath)

    # 把两个变量封装到上下文里
    context = {
        'imageResult': imageResult,
        'imageContent': imageContent,
    }
    # 把上下文传递到模板里
    return render(request, 'image.html', context)


def reptileArticle(request):
    print('============爬取文章信息==============')
    # 爬取文章信息

    # 爬取文章列表
    urlList = "http://www.576kk.com/xiaoshuoqu/jiqingxiaoshuo/"
    htmlList = requests.get(urlList)
    time.sleep(10)  # 睡眠十秒
    htmlList.encoding = 'utf-8'
    soupList = BeautifulSoup(htmlList.text, 'lxml')
    articleList = soupList.find_all('li')
    for link in articleList:
        # 爬取文章详细
        urlArticle = 'http://www.576kk.com/' + link.find('a').get('href')
        html = requests.get(urlArticle, timeout=30)
        time.sleep(10)  # 睡眠十秒
        htmlList.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, 'lxml')
        title = soup.find('h1', class_='h1-title').get_text()
        body = soup.find('div', class_='main-content').get_text()
        # 保存文章
        articleBean = Article()
        articleBean.body = body
        articleBean.title = title
        articleBean.save()
    return HttpResponse("操作成功")


def reptileImage(request):
    print('============爬取图片信息==============')
    # 爬取图片信息

    # 爬取图主题列表
    urlListImage = "http://www.576kk.com/tupianqu/YSE/"
    htmlListImage = requests.get(urlListImage)
    # time.sleep(10)  # 睡眠十秒
    htmlListImage.encoding = 'utf-8'
    soupListImage = BeautifulSoup(htmlListImage.text, 'lxml')
    articleList = soupListImage.find_all('li')
    for link in articleList:
        # 爬取图片详情
        urlImage = 'http://www.576kk.com/' + link.find('a').get('href')
        htmlImage = requests.get(urlImage, timeout=30)
        time.sleep(10)  # 睡眠十秒以防IP封锁
        htmlImage.encoding = 'utf-8'
        soup = BeautifulSoup(htmlImage.text, 'lxml')
        title = soup.find('h1', class_='h1-title').get_text()
        body = soup.find('div', class_='main-content')
        imageListP = body.find_all_next('p')
        imageNameList = ''
        # 对所有图片进行解析，保存
        for imageHref in imageListP:
            imgurl = imageHref.find('img').get('src')
            dir = os.path.abspath('./static/imgs')
            filename = os.path.basename(imgurl)
            if imageNameList == '':
                imageNameList = filename
            else:
                imageNameList = imageNameList + ',' + filename
            imgpath = os.path.join(dir, filename)
            print('开始下载 %s' % imgurl)
            download_file(imgurl, imgpath)
        print(title)
        print(imageNameList)
        # 保存图片
        imageBean = Image()
        imageBean.title = title
        imageBean.image_path = imageNameList
        imageBean.save()
    return HttpResponse("操作成功")


def reptileVideo(request):
    # 爬取视频信息

    # 爬取视频列表，好看视频时下热门
    urlListVideo = "https://haokan.baidu.com/tab/gaoxiao"
    htmlListVideo = requests.get(urlListVideo)
    time.sleep(10)  # 睡眠十秒
    htmlListVideo.encoding = 'utf-8'
    soupList = BeautifulSoup(htmlListVideo.text, 'lxml')
    videoListp = soupList.find('div', class_='recommend float-left')
    print(videoListp)
    videoList = videoListp.find_all_next('li')
    for link in videoList:
        # 爬取视频详细地址
        urlVideo = link.find('a').get('href')
        # print(urlVideo)
        html = requests.get(urlVideo)
        time.sleep(10)  # 睡眠十秒
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, 'lxml')
        videoHref = soup.find('video').get('src')
        videoTitle = soup.find('h2', class_='videoinfo-title').get_text()
        print(videoHref)
        print(videoTitle)
        # 下载视频
        dir = os.path.abspath('./static/video')
        filename = os.path.basename(videoHref)
        filenameArr = filename.split('?')
        filename = filenameArr[0]
        videoPath = os.path.join(dir, filename)
        print(filename)
        print('开始下载 %s' % videoPath)
        download_file(videoHref, videoPath)
        # 保存视频路径到数据库
        videoBean = Video()
        videoBean.title = videoTitle
        videoBean.video_path = 'video/' + filename
        videoBean.save()
    return HttpResponse("操作成功")


# 下载文件函数
def download_file(file_url, file_local_path):
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(file_local_path, 'wb') as f:
            response.raw.deconde_content = True
            shutil.copyfileobj(response.raw, f)
