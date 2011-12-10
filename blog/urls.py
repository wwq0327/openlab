from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('openlab.blog.views',
                       url(r'^$', 'entry_list', name="entry_lst"),
                       url(r'^entry/(?P<id>\d+)/', 'entry_page', name="entry_pg"),
                       url(r'^new/$', 'entry_new', name="entry_new"),
                       url(r'^tags/(\w+)', 'entry_tag', name='entry_tag'),
                       url(r'^edit/(?P<id>\d+)/', 'entry_edit', name='edtry_ed'),
                       url(r'^del/(?P<id>\d+)/', 'entry_del', name='edtry_del'),
                       )

urlpatterns += patterns('',
                        url(r'^comments/', include('django.contrib.comments.urls')),
                        )
