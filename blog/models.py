from django.db import models

from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Tag(models.Model):
    tag = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return '%s' % self.tag

class Category(models.Model):
    name = models.CharField(max_length=32)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return '%s, %s' % (self.name, self.user.username)

class Entry(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    updated = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category)

    def __str__(self):
        return '%s, %s' % (self.title, self.user.username)

    class Meta:
        ordering = ['-updated']

    def _get_slug(self):
        return slugify(self.title)




