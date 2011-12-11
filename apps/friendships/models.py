from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Friendship(models.Model):
    from_friend = models.ForeignKey(User, related_name='friend_set')
    to_friend = models.ForeignKey(User, related_name='to_friend_set')

    def __str__(self):
        return '%s, %s' % (self.from_friend.username, self.to_friend.username)

    class Meta:
        unique_together = (('to_friend', 'from_friend'), )

