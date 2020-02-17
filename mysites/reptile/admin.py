from django.contrib import admin
from .models import Video, Article, Image


# 导入需要管理的数据库表

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'video_path', 'created_time', 'modified_time')
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-created_time',)
    # 后台数据列表排序方式
    list_display_links = ('id', 'title')

    # 设置哪些字段可以点击进入编辑界面

    @admin.register(Article)
    class ArticleAdmin(admin.ModelAdmin):
        list_display = ('id', 'title', 'body', 'created_time', 'modified_time')
        # 文章列表里显示想要显示的字段
        list_per_page = 50
        # 满50条数据就自动分页
        ordering = ('-created_time',)
        # 后台数据列表排序方式
        list_display_links = ('id', 'title')

        # 设置哪些字段可以点击进入编辑界面

        @admin.register(Image)
        class ArticleAdmin(admin.ModelAdmin):
            list_display = ('id', 'title', 'image_path', 'created_time', 'modified_time')
            # 文章列表里显示想要显示的字段
            list_per_page = 50
            # 满50条数据就自动分页
            ordering = ('-created_time',)
            # 后台数据列表排序方式
            list_display_links = ('id', 'title')
            # 设置哪些字段可以点击进入编辑界面
