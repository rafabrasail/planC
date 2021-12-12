from django.db import models
# from django.contrib.auth.models import User
# from users.models import User
from posts.models import Post

from django.db.models.signals import post_save

from PIL import Image
from django.conf import settings
import os
from django.contrib.auth import get_user_model
User = get_user_model()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    profile_pic_name = 'user_{0}/profile.png'.format(instance.user.id)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_pic_name


class Profile(models.Model):
    FOOT = (
        ("E", "Left"),
        ("D", "Right"),
        ("B", "Both")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=80, null=True, blank=True)
    profile_info = models.TextField(max_length=150, null=True, blank=True)
    born = models.DateField(auto_now_add=False, null=True, blank=True)
    favorite_foot = models.CharField(max_length=1, choices=FOOT, default="E")
    club = models.CharField(max_length=50, null=True, blank=True)
    favorites = models.ManyToManyField(Post)
    picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Picture')    
    created = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now_add=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SIZE = 250, 250
        
        if self.picture:
            pic = Image.open(self.picture.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.picture.path)

    def __str__(self):
        return self.user.username


    # def get_user_model():
    #     try:
    #         return author.get_model(settings.AUTH_USER_MODEL, require_ready=False)
    #     except ValueError:
    #         raise ImproperlyConfigured(
    #             "AUTH_USER_MODEL must be of the form 'app_label.model_name'")
    #     except LookupError:
    #         raise ImproperlyConfigured(
    #             "AUTH_USER_MODEL refers to model '%s' that has not been installed" % settings.AUTH_USER_MODEL
    #         )

