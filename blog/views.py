from django.shortcuts import render
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View
from blog.models import Article, Category, Tag
from django.conf import settings
from django.http import HttpResponseRedirect


class IndexView(ListView):
    template_name = 'blog/list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        # 过滤处 staus 为 p 的文章
        articles = Article.objects.filter(status='p')
        return articles

    # 理解 get_context_data() 函数作用
    def get_context_data(self, **kwargs):
        # 给 context 对象添加额外的内容并且传递给视图函数
        kwargs['title'] = '首页'
        return super(IndexView, self).get_context_data(**kwargs)


# 分类视图
class CategoryView(ListView):
    template_name = 'blog/list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        category_id = int(self.kwargs['category_id'])
        if category_id == 0:
            articles = Article.objects.filter(category__isnull=True, status='p')
        else:
            articles = Article.objects.filter(category=category_id, status='p')
        return articles

    def get_context_data(self, **kwargs):
        try:
            kwargs['title'] = '分类:' + Category.objects.filter(pk=self.kwargs['category_id'])[0].title
        except IndexError:
            kwargs['title'] = '没有找到这个分类!'
        return super(CategoryView, self).get_context_data(**kwargs)


# 标签视图
class TagView(ListView):
    template_name = 'blog/list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        articles = Article.objects.filter(tag=self.kwargs['tag_id'], status='p')
        return articles

    def get_context_data(self, **kwargs):
        try:
            kwargs['title'] = '标签:' + Tag.objects.filter(pk=self.kwargs['tag_id'])[0].title
        except IndexError:
            kwargs['title'] = '没有找到标签!'
        return super(TagView, self).get_context_data(**kwargs)




# 文章详情视图
class ArticleDetailView(DetailView):
    model = Article
    # 指定的渲染模板
    template_name = 'blog/post.html'
    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'article'

    # 这里注意，pk_url_kwarg用于接收一个来自url中的主键，然后会根据这个主键进行查询
    # 我们之前在urlpatterns已经捕获article_id
    pk_url_kwarg = 'article_id'

    # 指定以上几个属性，已经能够返回一个DetailView视图了
    def get_object(self):
        obj = super(ArticleDetailView, self).get_object()
        if obj.status == 'p':
            '''这里是什么意思'''
            obj.viewed()
            return obj

    def get_context_data(self, **kwargs):
        # 增加额外的数据，这里返回一个文章标题，以字典的形式
        kwargs['title'] = super(ArticleDetailView, self).get_object().title
        # 注意是 ArticleDetailView
        return super(ArticleDetailView, self).get_context_data(**kwargs)



