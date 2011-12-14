from django.db import models

from django.contrib.auth.models import User

class Status(models.Model):
    content = models.CharField(max_length=140)
    #content = models.TextField()
    updated = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return '%s, %s' % (self.content, self.user.username)

    class Meta:
        ordering = ['-updated']


