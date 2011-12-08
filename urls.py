from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       # all home of the site
                       (r'^$', 'openlab.accounts.views.all_home'),
                       # accounts mananger
                       (r'^accounts/', include('openlab.accounts.urls')),
    # Examples:
    # url(r'^$', 'openlab.views.home', name='home'),
    # url(r'^openlab/', include('openlab.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
