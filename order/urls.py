from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('order.views',
    url(r'^create', 'create'),
    url(r'^list/order', 'listOrder'),
    url(r'^csv', 'importDataFormCSV')
)
