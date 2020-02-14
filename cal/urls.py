from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'cal'
urlpatterns = [
    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path('delete_event/<int:pk>/', views.EventDeleteView.as_view(), name = 'event_delete'),
]