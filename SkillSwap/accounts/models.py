from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    
    #relation for django model user and our userprofileform model
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    avatar = models.ImageField(upload_to="images/", blank=True, null=True)

    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def offered_skills(self):
        return self.user.offered_skills.all()

    def needed_skills(self):
        return self.user.needed_skills.all()
    