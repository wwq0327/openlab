from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('openlab.blog.views',
                       url(r'^$', 'entry_list', name="entry_lst"),
                       url(r'^entry/(?P<id>\d+)/', 'entry_page', name="entry_pg"),
                       url(r'^new/$', 'entry_new', name="entry_new"),
                       )
