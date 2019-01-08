from django import forms
from .models import Message,Topic,Tag
from tinymce.widgets import TinyMCE
from django.core.exceptions import ValidationError
class MessageForm(forms.Form):
    message = forms.CharField(label="",widget=TinyMCE())
class CreateTopicForm(forms.ModelForm):
    message =  forms.CharField(label="", required=True, widget=TinyMCE())
    tags = forms.CharField(required=True)
    class Meta:
        model = Topic
        fields =('theme',)

    def get_tags(self):
        return [Tag.objects.get(name=i) for i in self.cleaned_data['tags'].replace(' ', '').split(',')]

    def clean(self):
        cd = self.cleaned_data
        tags = cd['tags'].replace(' ', '').split(',')
        for tag in tags:
            if  not Tag.objects.filter(name=tag).exists():
                self.add_error('tags', "check your tags!")
                raise ValidationError("")
        return cd