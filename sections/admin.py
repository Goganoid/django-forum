from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth import get_user_model
User = get_user_model()
class SubForumInline(admin.TabularInline):
    model = SubForum
    extra = 0
class MessageInline(admin.StackedInline):
    model = Message
    fields = ('creator','text')
    readonly_fields = fields
    extra = 0
class TopicInlineTag(admin.TabularInline):
    model = Topic.tags.through
    extra = 0
class TopicInline(admin.TabularInline):
    model = Topic
    fields = ('theme','views','tags','time_created','creator')
    readonly_fields = fields
    extra = 0
class ForumAdmin(admin.ModelAdmin):
    inlines = [SubForumInline]

class TagAdmin(admin.ModelAdmin):
    inlines = [TopicInlineTag]
class SubForumAdmin(admin.ModelAdmin):
    inlines = [TopicInline]
class TopicAdmin(admin.ModelAdmin):
    list_display = ('theme','views','time_created','subforum')
    inlines = [MessageInline]
    readonly_fields = ['views',]


admin.site.register(Forum,ForumAdmin)
admin.site.register(Topic,TopicAdmin)
admin.site.register(User)
admin.site.register(SubForum,SubForumAdmin)
admin.site.register(Tag,TagAdmin)