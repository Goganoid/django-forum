from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2','about','profile_image')
        widgets ={
            'about':forms.Textarea
        }

    def save(self,commit=True):
        # print(self.cleaned_data)
        user = super(RegisterForm,self).save(commit=False)
        # user.profile_image = self.cleaned_data['profile_image']
        user.set_password(self.cleaned_data['password1'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.about = self.cleaned_data['about']
        if commit:
            user.save()
        return user