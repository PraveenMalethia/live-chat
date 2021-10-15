from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# thread class with two user foreignkeys 
class Thread(models.Model):
    user1 = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user2')
    # add a string field to the model

class Message(models.Model):
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE, related_name='thread')
    sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.sender.username + ': ' + self.message