from django.views import generic,View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,render,reverse
from django.urls import reverse_lazy
from .models import Forum,SubForum,Topic,Message,Tag
from .forms import MessageForm, CreateTopicForm
from django.contrib.auth.mixins import LoginRequiredMixin
class IndexView(View):
    template_name = 'sections/index.html'
    context_object_name = 'forums'
    def get(self,request):
        return render(request,self.template_name, {'forums': Forum.objects.order_by('name'),
                                                   'last_topics': Topic.objects.order_by('-time_created')[:4]
                                                  })


class SubForumView(generic.DetailView):
    template_name = 'sections/subforum.html'
    context_object_name = 'subforum'
    model = SubForum


class TopicView(View):
    template_name = 'sections/topic.html'
    model = Topic
    form_class = MessageForm

    def get(self,request,**kwargs):
        topic = get_object_or_404(Topic,pk=kwargs['pk'])
        topic.views+=1
        topic.save()
        return render(request,self.template_name,{'topic':topic,'form':self.form_class})

    def post(self,request,**kwargs):
        print(request.POST)
        print(kwargs)
        message = request.POST.get('message', None)
        topic = Topic.objects.get(pk=kwargs['pk'])
        message = Message.objects.create(
            creator=request.user,
            topic=topic,
            text=message
        )
        message.save()
        data = {
            'creator': message.creator.username,
            'message': message.text,
            'time_created': message.time_created.strftime('%b. %d, %Y, %I:%M %p')
        }
        return JsonResponse(data)


class CreateTopicView(LoginRequiredMixin,generic.FormView):
    login_url = '/login/'
    template_name = 'sections/createanswer.html'
    form_class = CreateTopicForm

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,{
            'form': self.form_class,
            'tags': [tag.name for tag in Tag.objects.all()],
            'pk':kwargs['pk']
        })

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            tags = form.get_tags()
            topic = Topic.objects.create(
                subforum=SubForum.objects.get(pk=kwargs['pk']),
                theme=form.cleaned_data['theme'],
                creator=request.user)
            for tag in tags:
                topic.tags.add(tag)
            message = Message.objects.create(
                creator=request.user,
                text=form.cleaned_data['message'],
                topic=topic,
            )
            topic.save()
            message.save()
            return JsonResponse({
                'redirect_url': reverse('topic',args=(topic.id,))
            })
        else:
            return JsonResponse({
                'errors_list':form.errors
            })