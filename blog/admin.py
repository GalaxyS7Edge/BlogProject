from django.contrib import admin
from .models import Post, Category, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author', 'object_link']
    list_filter = ['created_time']
    search_fields = ['title', 'body']
    list_select_related = True

    def object_link(self, item):
        url = item.get_absolute_url()
        return u'<a href={url}>查看</a>'.format(url=url)

    object_link.short_description = '查看站点'
    object_link.allow_tags = True

    class Media:
        js = (
            '/static/js/editor/kindeditor-4.1.11/kindeditor-all.js',
            '/static/js/editor/kindeditor-4.1.11/lang/zh_CN.js',
            '/static/js/editor/kindeditor-4.1.11/config.js'
        )

# 把新增的 PostAdmin 也注册进来
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
