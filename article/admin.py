from django.contrib import admin

from .models import Article, Category, Tag, Avatar

# 把Article模型注册到管理后台
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Avatar)