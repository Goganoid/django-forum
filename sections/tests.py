from django.test import TestCase,RequestFactory

from django.shortcuts import reverse

from .models import SubForum,Forum,Topic,Tag,Message
from .forms import MessageForm
from .views import CreateTopicView

from django.contrib.auth import get_user_model
from django.test import Client
User = get_user_model()
# Create your tests here.
class SectionTests(TestCase):
    def create_tag(self,name):
        return Tag.objects.create(name=name)

    def create_topic(self,subforum,creator,tags,theme="TopicTheme"):
        topic = Topic.objects.create(subforum=subforum,theme=theme, creator=creator)
        if tags:
            for tag in tags:
                topic.tags.add(tag)
        return topic

    def setUp(self):
        self.tags = [self.create_tag('tag1'),self.create_tag('tag2'),self.create_tag('tag3')]
        self.subforum = SubForum.objects.create( section = Forum.objects.create())
        self.request_factory = RequestFactory()
        self.user = User.objects.create(username="User", password="testpassword")
        self.topic = self.create_topic(self.subforum,self.user,self.tags)
        self.message = Message.objects.create(creator = self.user, topic = self.topic, text = "TestText")
        self.client = Client()
        self.client.login(username="User", password="testpassword")

    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code,200)

    def test_last_themes(self):

        self.create_topic(self.subforum,self.user,self.tags,'TopicTheme1')
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(response.context['last_topics'],['<Topic: TopicTheme1>','<Topic: TopicTheme>'])

    def test_subforum_page(self):
        response = self.client.get(reverse('subforum',args=(self.subforum.id,)))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,self.subforum.name)
    def test_suborum_page_contains_topics(self):

        response = self.client.get(reverse('subforum', args=(self.subforum.id,)))
        self.assertContains(response,self.topic.theme)
    def test_topic_contains_messages(self):

        response = self.client.get(reverse('topic',args=(self.topic.id,)))
        self.assertContains(response,self.message.text)
    def test_message_get_time_created(self):

        self.assertEqual(self.message.get_time_created(),self.message.time_created.strftime('%b. %d, %Y, %I:%M %p'))
    def test_anon_user_has_no_access_to_message_form(self):

        response = self.client.get(reverse('topic',args=(self.topic.id,)))
        self.assertContains(response,
                            '<p>Please <li><a href="%s">Login</a> or <a href="%s">Register</a></li></p>' % (reverse('auth:login'),reverse('auth:register')))
    def test_anon_user_has_no_access_to_create_topic_form(self):

        response = self.client.get(reverse('createtopic',args=(self.subforum.id,)))
        self.assertContains(response,
                            '<p>Please <li><a href="%s">Login</a> or <a href="%s">Register</a></li></p>' % (reverse('auth:login'),reverse('auth:register')))
    def test_logged_user_access_to_message_form(self):

        response = self.client.get(reverse('topic',args=(self.topic.id,)))
        self.assertEqual(response.context['form'],MessageForm)

    def test_logged_user_access_to_create_topic_form(self):
        response = self.client.get(reverse('topic', args=(self.topic.id,)))
        self.assertEqual(response.context['form'], MessageForm)

    def test_create_topic_form_redirects(self):
        print('tags',','.join([tag.name for tag in self.tags]))
        request = self.request_factory.post(reverse('createtopic',args=(self.subforum.id,)),{
             'theme': 'Theme',
             'message': 'Text',
             'tags': ','.join([tag.name for tag in self.tags])
        })
        request.user = self.user
        response = CreateTopicView.as_view()(request,pk=self.subforum.id)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'redirect_url': reverse('topic', args= (Topic.objects.get(theme='Theme').id,))}
        )

    def test_create_topic_context_has_tags(self):
        response = self.client.get(reverse('createtopic',args=(self.subforum.id,)))
        self.assertEqual(response.context['tags'], [tag.name for tag in self.tags])






