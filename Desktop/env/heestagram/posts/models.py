from email.mime import image
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):

        user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
        body = models.TextField()
        image = models.ImageField(upload_to='posts', null=True)
        created_at = models.DateTimeField()
        liked_users = models.ManyToManyField(User, related_name='liked_posts')

        def __str__(self):
            if self.user:
                return f'{self.user.get_username()}: {self.body}'
            else:
                return f'{self.body}'
