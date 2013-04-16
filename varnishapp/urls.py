from django.conf.urls.defaults import *
from views import ManagementView

urlpatterns = patterns('varnishapp.views',
    (r'', ManagementView.as_view()),
)
