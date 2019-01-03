from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
def content_file_name(instance, filename):
    # print('profiles/'+instance.user.id+filename.split('.')[1])
    print(instance)
    return 'profiles/'+instance.username+'.' + filename.split('.')[1]


class User(AbstractUser):
    last_activity = models.DateTimeField(null=True)
    about = models.CharField(max_length=400,default="",blank=True)
    profile_image = models.FileField(upload_to=content_file_name,
                                     default='profiles/profile_standart.png',
                                     blank=True,
                                     validators=[FileExtensionValidator(allowed_extensions=['jpg','png'])],
                                     max_length=500)
    def get_full_name(self):
        return self.first_name+" "+self.last_name+" "
