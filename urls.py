from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       # all home of the site
                       url(r'^$', 'openlab.apps.accounts.views.all_home', name='index'),
                       url(r'^(?P<username>\w+)/home/$', 'openlab.apps.accounts.views.home', name='home'),
                       # accounts mananger
                       url(r'^accounts/', include('openlab.apps.accounts.urls')),
                       # blog
                       url(r'^(?P<username>\w+)/blog/', include('openlab.apps.blog.urls'), name='blog'),
                       #url(r'^$', include('openlab.status.urls')),
                       url(r'^(?P<username>\w+)/home/st/(?P<id>\d+)/del/$', 'openlab.apps.status.views.st_del_page', name='st_del'),

                       #friendships
                       url(r'^(?P<username>\w+)/friends/', include('openlab.apps.friendships.urls')),
                       url(r'^comments/', include('django.contrib.comments.urls')),

                       )
