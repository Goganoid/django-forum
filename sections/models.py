from django.db import models
from tinymce.models import HTMLField
from django.conf import settings
# Create your models here.


class Forum(models.Model):
    name = models.CharField(max_length=30,default="Undefined Name")
    def __str__(self):
        return self.name


class SubForum(models.Model):
    section = models.ForeignKey(Forum,on_delete=models.CASCADE)
    name = models.CharField(max_length=30,default="Undefined Name")
    def total_messages(self):
        messages=0
        for topic in self.topic_set.all():
            messages+=topic.message_set.count()
        return messages
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=75)
    def get_topics(self):
        return Topic.objects.filter(tags__name=self.name)
    def __str__(self):
        return self.name
class Topic(models.Model):
    subforum = models.ForeignKey(SubForum,on_delete=models.CASCADE)
    theme = models.CharField(max_length=200)
    views = models.PositiveIntegerField(default=0,)
    time_created = models.DateTimeField(auto_now_add=True, blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,blank=False)
    def __str__(self):
        return self.theme
    def getSubForum(self):
        return self.subforum


class Message(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,default='')
    text = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True, blank=True)
    def get_time_created(self):
        return self.time_created.strftime('%b. %d, %Y, %I:%M %p')
    def __str__(self):
        return self.text[:30]+'...'
