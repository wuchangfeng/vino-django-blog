#-*- coding: UTF-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from django.conf import settings


class Article(models.Model):

    STATUS_CHOICES = (
        ('p', '发布'),
        ('t', '草稿'),
        ('d', '删除'),
    )
    title = models.CharField('标题', max_length=100)
    body = models.TextField('文章显示')
    text = models.TextField('原文', default='')
    description = models.CharField('摘要', max_length=140, blank=True, null=True,
                                   help_text='可选，为空则自动选取前140个字符')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag', verbose_name='标签', blank=True)
    category = models.ForeignKey('Category', verbose_name='分类', blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField('状态', max_length=1, choices=STATUS_CHOICES, default='p')
    time_create = models.DateTimeField('发布时间', default=timezone.now)
    time_last_modified = models.DateTimeField('修改时间', auto_now=True)
    views = models.PositiveIntegerField('浏览量', default=0)

    def __str__(self):
        return self.title

    class Meta:
        # 根据创建时间倒叙输出
        ordering = ['-time_create']
        verbose_name = '文章数据'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):

        return reverse('blog:detail', kwargs={'article_id': self.pk})


    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_previous_article(self):

        all_item = Article.objects.filter(status='p').order_by('id')
        index = 0
        for x in all_item:
            if x.id == self.id:
                break
            else:
                index += 1
        if index:
            return all_item[index - 1]

    def get_next_article(self):

        all_item = Article.objects.filter(status='p').order_by('-id')
        index = 0
        for x in all_item:
            if x.id == self.id:
                break
            else:
                index += 1
        if index:
            return all_item[index - 1]


# 分类模型
class Category(models.Model):
    title = models.CharField('标题', max_length=40)
    order = models.IntegerField('排序', default=0)
    description = models.CharField('摘要', max_length=140, blank=True, null=True, default='一个分类')
    time_create = models.DateTimeField('创建时间', default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_create']
        verbose_name = '分类数据'
        verbose_name_plural = verbose_name


    def p_count(self):
        """分类下发布状态的文章数量"""
        count = self.article_set.filter(status='p').count()
        return count


# 标签模型
class Tag(models.Model):
    title = models.CharField('标题', max_length=40)
    order = models.IntegerField('排序', default=0)
    time_create = models.DateTimeField('创建时间', default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_create']
        verbose_name = '标签数据'
        verbose_name_plural = verbose_name

