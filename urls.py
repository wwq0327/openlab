from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       # all home of the site
                       url(r'^$', 'openlab.accounts.views.all_home', name='index'),
                       url(r'^(?P<username>\w+)/home/$', 'openlab.accounts.views.home', name='home'),
                       # accounts mananger
                       url(r'^accounts/', include('openlab.accounts.urls')),
                       # blog
                       url(r'^(\w+)/blog/', include('openlab.blog.urls')),
                       #url(r'^$', include('openlab.status.urls')),
                       url(r'^(?P<username>\w+)/home/st/(?P<id>\d+)/del/$', 'openlab.status.views.st_del_page', name='st_del'),

                       )
