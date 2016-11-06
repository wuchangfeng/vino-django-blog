
#-*- coding: UTF-8 -*-
from django.contrib import admin, messages
from blog.models import Article, Category, Tag
from django.conf import settings
import markdown2
from django import forms
from  pagedown.widgets import AdminPagedownWidget


# Register your models here.


# 文章模型定制
class MarkdownForm(forms.ModelForm):
    text = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Article
        fields = '__all__'


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'time_last_modified', 'views')
    actions = ('make_publish', 'make_temp', 'make_delete')
    form = MarkdownForm

    def make_publish(self, request, queryset):
        num = queryset.update(status='p')
        message = "%s 篇文章已经标记为发布状态" % num
        messages.success(request, message=message)

    make_publish.short_description = '将文章设置为发布状态'

    def make_temp(self, request, queryset):
        num = queryset.update(status='t')
        message = "%s 篇文章已经标记为草稿状态" % num
        messages.success(request, message=message)

    make_temp.short_description = '将文章设置为草稿状态'

    def make_delete(self, request, queryset):
        num = queryset.update(status='d')
        message = "%s 篇文章已经标记为删除状态" % num
        messages.success(request, message=message)

    make_delete.short_description = '将文章设置为删除状态'

    def save_model(self, request, obj, form, change):
        if settings.MARKDOWN:
            obj.body = markdown2.markdown(obj.text, extras=['fenced-code-blocks'], )  # 处理markdown文章
        else:
            obj.body = obj.text
        obj.description = obj.description or markdown2.markdown(obj.text[:140], extras=['fenced-code-blocks'], )  # 描述
        obj.author = request.user  # 获取文章发布者
        obj.save()

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'text',)
        }),
        ('更多', {
            'fields': ('category', 'tag'),
        }),
        ('其他', {
            'fields': ('status', 'time_create', 'views'),
            'classes': ['collapse'],
        }),
    )

    class Media:
        if settings.MARKDOWN:
            js = ['blog/js/pagedown/js/custom.js']
        else:
            js = ['blog/js/tinymce/tinymce.min.js', 'blog/js/tinymce/textareas.js']


# 分类模型定制
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'description', 'time_create')

    fieldsets = (
        ('基本设置', {
            'fields': ('title', 'description', 'order')
        }),
    )


# 标签模型定制
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')

    fieldsets = (
        ('基本设置', {
            'fields': ('title', 'order')
        }),
    )

# 向 admin 注册
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)

