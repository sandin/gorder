from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('order.views',
    url(r'^create', 'create'),
    url(r'^delete/(\d+)$', 'delete'),
    url(r'^list/jiahe', 'listOrder2'),
    url(r'^list$', 'listOrder'),
    url(r'^csv', 'importDataFormCSV'),
    url(r'^(\d+)$', 'orderDetail'),
)
