# -*- encoding:utf-8 -*-
from __future__ import print_function

import markdown

from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse
from django.utils.html import strip_tags
from datetime import datetime
from django.utils import timezone
from textrank4zh import TextRank4Keyword, TextRank4Sentence


# python_2_unicode_compatible 装饰器用于兼容 Python2
@python_2_unicode_compatible
class Category(models.Model):
    """
    Django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    当然 Django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
    Django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100, verbose_name='分类')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    """
    标签 Tag 也比较简单，和 Category 一样。
    再次强调一定要继承 models.Model 类！
    """
    name = models.CharField(max_length=100, verbose_name='标签')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    """
    文章的数据库表稍微复杂一点，主要是涉及的字段更多。
    """

    # 文章标题
    title = models.CharField(max_length=70, verbose_name='标题')

    # 文章正文，我们使用了TextField。
    # 存储比较短的字符串可以使用CharField，但对于文章的正文来说可能会是一大段文本，因此使用TextField。
    body = models.TextField(verbose_name='内容')

    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用DateTimeField类型。
    created_time = models.DateTimeField(verbose_name='创建时间', editable=False)
    modified_time = models.DateTimeField(verbose_name='修改时间', editable=False)

    # 文章摘要，可以没有文章摘要，但默认情况下CharField要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank = True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=300, verbose_name='摘要', blank=True)

    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/1.10/topics/db/models/#relationships
    category = models.ForeignKey(Category, verbose_name='分类')
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(User, verbose_name='作者')

    # 新增 views 字段记录阅读量
    views = models.PositiveIntegerField(verbose_name='阅读量', default=0)

    # 文章配图
    img = models.ImageField(upload_to='image/%Y/%m/%d/', verbose_name='标题配图', blank=True)

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 阅读量函数
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 重写 save 函数，如果没有输入摘要就自动提取文章前54个字作为摘要存储到数据库
    def save(self, *args, **kwargs):
        # 如果没有写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            # self.excerpt = strip_tags(md.convert(self.body))[:50]
            tr4s = TextRank4Sentence()
            # tr4w = TextRank4Keyword()
            tr4s.analyze(text=strip_tags(md.convert(self.body)), lower=True, source='all_filters')
            # tr4w.analyze(text=strip_tags(md.convert(self.body)), lower=True, window=2)
            for item in tr4s.get_key_sentences(num=1):
                self.excerpt += (item.sentence + "。")
            self.excerpt = "摘要：" + self.excerpt
        if not self.id:
            self.created_time = timezone.now()
        self.modified_time = timezone.now()

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_time']
