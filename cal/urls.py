from django.conf.urls import url
from django.urls import path, re_path
from . import views

app_name = 'cal'
urlpatterns = [
    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    path('calendar/event/new/<str:datum>/', views.EventNewFromCalView.as_view(), name='new_event_from_cal'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path('delete_event/<int:pk>/', views.EventDeleteView.as_view(), name = 'event_delete'),
    path('list_events/<str:choice>/', views.EventChoiceListView.as_view(), name = 'event_choice_list'),
]