from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('openlab.apps.blog.views',
                       url(r'^$', 'entry_list', name="entry_lst"),
                       url(r'^entry/(?P<id>\d+)/$', 'entry_page', name="entry_pg"),
                       url(r'^new/$', 'entry_new', name="entry_new"),
                       url(r'^tags/(?P<tag>\w+)/$', 'entry_tag', name='entry_tag'),
                       url(r'^edit/(?P<id>\d+)/$', 'entry_edit', name='edtry_ed'),
                       url(r'^del/(?P<id>\d+)/$', 'entry_del', name='edtry_del'),
                       url(r'^category/(?P<id>\d+)/del/$', 'category_del', name='cg_del'),
                       url(r'^category/$', 'category_list', name='cg_list'),
                       url(r'^category/(?P<id>\d+)/$', 'category_entry', name='cg_entry'),
                       )

## urlpatterns += patterns('',
##                         url(r'^comments/', include('django.contrib.comments.urls')),
##                         )
