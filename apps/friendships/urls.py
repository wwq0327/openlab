from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('openlab.apps.friendships.views',
                       url(r'^$', 'friends_page'),
                       url(r'^add/$', 'friend_add'),
                       )
