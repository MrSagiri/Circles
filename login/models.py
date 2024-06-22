from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
import os


class friend(models.Model):
    name = models.CharField(max_length=100)

def user_profile_path(instance, filename):
    return f'Profile/{instance.username}/{filename}'
    
class newAcc(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    id = models.AutoField(primary_key=True, auto_created=True)
    image = models.ImageField(upload_to= user_profile_path, null=False, blank=True, default='')
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    username = models.CharField(max_length = 10, default = "")
    # password = models.CharField(max_length = 10, default = "")
    # password2 = models.CharField(max_length = 10, default = "")
    birthday = models.DateField(
        help_text = "Enter your birthday"
    )
    MALE = 'Male'
    FEMALE = 'Female'
    BISEXUAL = 'Bisexual'
    GAY = 'Gay'
    FEMBOY = 'Femboy'
    TRAP = 'Trap'

    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (BISEXUAL, 'Bisexual'),
        (GAY, 'Gay'),
        (FEMBOY, 'Femboy'),
        (TRAP, 'Trap')
    ]
    sex = models.CharField(
        max_length=8,
        choices=SEX_CHOICES,
        default=MALE,
    )
    address = models.CharField(max_length = 100)
    bio = models.CharField(max_length = 140, null=False, default = "")
    created_at = models.DateTimeField(auto_now_add=True, null = False)
    friends = models.ManyToManyField(friend)
    verified = models.BooleanField(default = False)
    def __str__(self):
        return f"{self.username}'s Profile"

class Posts(models.Model):
    image = models.TextField()
    author = models.CharField(max_length = 30, default = "")
    content = models.CharField(max_length = 100)
    created = models.DateTimeField(auto_now_add=True, null = False)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.author + " Post"    
    
    def total_likes(self):
        return self.likes.count()