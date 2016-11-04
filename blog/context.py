
#-*- coding: UTF-8 -*-
from .models import Category, Tag, Article
from django.conf import settings


# 全局使用参数
def all_context(request):

    categories = Category.objects.all().order_by('-order')
    tags = Tag.objects.all().order_by('-order')
    null_count = Article.objects.filter(category__isnull=True, status='p').count()
    paginate_num = settings.SITE_PAGINATE_NUM
    SITE_NAME = settings.SITE_NAME
    SITE_MASTER = settings.SITE_MASTER
    SITE_SIGNATURE = settings.SITE_SIGNATURE
    DUOSHUO_SHORT_NAME = settings.DUOSHUO_SHORT_NAME
    DUOSHUO_NEW_COMMENTS = settings.DUOSHUO_NEW_COMMENTS
    COLORTAG = settings.COLORTAG
    FRIENDLINK = settings.FRIENDLINK
    return locals()
