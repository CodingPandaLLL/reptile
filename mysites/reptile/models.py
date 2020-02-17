from django.db import models
from DjangoUeditor.models import UEditorField  # 头部增加这行代码导入UEditorField


# 文章
class Article(models.Model):
    title = models.CharField('标题', max_length=200)
    body = models.TextField()
    # body = UEditorField('内容', width=800, height=500,
    #                     toolbars="full", imagePath="upimg/", filePath="upfile/",
    #                     upload_settings={"imageMaxSize": 1204000},
    #                     settings={}, command=None, blank=True
    #                     )
    created_time = models.DateTimeField('发布时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)


class Meta:
    verbose_name = '文章'
    verbose_name_plural = '文章'


def __str__(self):
    return self.title


# 图片
class Image(models.Model):
    title = models.CharField('标题', max_length=200)
    image_path = models.CharField('图片路径', max_length=500)
    created_time = models.DateTimeField('发布时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)


class Meta:
    verbose_name = '图片'
    verbose_name_plural = '图片'


def __str__(self):
    return self.title


# 视频
class Video(models.Model):
    title = models.CharField('标题', max_length=200)
    video_path = models.CharField('视频路径', max_length=500)
    created_time = models.DateTimeField('发布时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)


class Meta:
    verbose_name = '视频'
    verbose_name_plural = '视频'


def __str__(self):
    return self.title
