from django.db import models

from django.contrib.auth.models import User

class Entry(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    content = models.TextField()
    updated = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return '%s, %s' % (self.title, self.user.username)

    class Meta:
        ordering = ['-updated']




