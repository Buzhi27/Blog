from django.db import models
# timezone模块提供了与时区相关的功能
from django.utils import timezone
from django.contrib.auth.models import User
from markdown import Markdown


class Tag(models.Model):
    """文章标签"""
    text = models.CharField(max_length=30)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text


class Category(models.Model):
    """文章分类"""
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Avatar(models.Model):
    content = models.ImageField(upload_to='avatar/%Y%m%d')


class Article(models.Model):
    # 分类
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )

    # 标签
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='articles'
    )

    # 标题图
    avatar = models.ForeignKey(
        # 指向模型 Avatar
        Avatar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles'

    )


    # 博客文章model
    author = models.ForeignKey(
        User,
        null=True,
        # 表示在关联的用户对象被删除时，与之关联的文章对象也会被删除
        on_delete=models.CASCADE,
        # 表示通过用户对象可以反向查询到其所有的文章
        related_name='articles'
    )
    # 标题
    title = models.CharField(max_length=100, default="Default Title")
    # 正文
    body = models.TextField(default="Default Body")
    # 创建时间,设置默认值为当前时间。
    created = models.DateTimeField(default=timezone.now)
    # 更新时间,auto_now=True 表示这个字段会在每次模型保存时自动更新为当前时间。
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']


    def get_md(self):
        md = Markdown(
            extensions=[
                # 额外的语法支持
                'markdown.extensions.extra',
                # 代码高亮
                'markdown.extensions.codehilite',
                # 生成目录
                'markdown.extensions.toc',
            ]
        )
        # 将正文内容转换成Markdown格式，然后将结果保存在 md_body 中
        md_body = md.convert(self.body)
        # toc 是渲染后的目录
        return md_body, md.toc




    