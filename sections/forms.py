from django import forms
from .models import Message,Topic,Tag
class MessageForm(forms.Form):
    message = forms.CharField(label="",widget=forms.Textarea(attrs={
        'id':'message-text'
    }))
class CreateTopicForm(forms.ModelForm):
    message =  forms.CharField(label="", required=True, widget=forms.Textarea())
    tags = forms.CharField(required=True)
    class Meta:
        model = Topic
        fields =('theme',)

    def get_tags(self):
        print(self.cleaned_data['tags'].replace(' ', ''))
        print(self.cleaned_data['tags'])
        print(self.cleaned_data['tags'].replace(' ', '').split(','))
        return [Tag.objects.get(name=i) for i in self.cleaned_data['tags'].replace(' ', '').split(',')]