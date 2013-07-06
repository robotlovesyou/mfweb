from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login

from gigs import views

urlpatterns = patterns(
    '',
    url(r'^login/$', login, name='login'),
    url(r'^admin/$', views.admin, name='admin'),
    url(
        r'^admin/create/$',
        login_required(views.GigCreateView.as_view()),
        name='admin_create'
    ),
    url(
        r'admin/update/(?P<pk>\d+)/$',
        login_required(views.GigUpdateView.as_view()),
        name='admin_update'
    ),
    url(
        r'admin/delete/(?P<pk>\d+)/$',
        login_required(views.GigDeleteView.as_view()),
        name='admin_delete'
    ),
    #url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    #url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)
