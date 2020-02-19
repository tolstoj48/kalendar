# cal/views.py

from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.utils.safestring import mark_safe
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView, CreateView

from .forms import EventForm
from .models import *
from .utils import Calendar
import datetime
import calendar

class CalendarView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        context['months_for_loop'] = range(1, 12)

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.date.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - datetime.timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + datetime.timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


@login_required
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        first_part_link = reverse('cal:calendar')
        str_for_link = "?month=" + str(instance.start_time)[:7]
        return HttpResponseRedirect(first_part_link + str_for_link)
    return render(request, 'event.html', {'form': form})


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'event_delete.html'
    #success_url = reverse_lazy('cal:calendar')
    
    def get_success_url(self):
        id_object = self.kwargs['pk']
        instance = get_object_or_404(Event, pk=id_object)
        first_part_link = reverse('cal:calendar')
        second_part_link = "?month=" + str(instance.start_time)[:7]
        return first_part_link + second_part_link

class EventNewFromCalView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'event.html'
    fields = ['title','type_of_events', 'description', 'start_time', 'end_time', 'user', ]

    def get_initial(self, **kwargs):
        days, months, years = self.kwargs['datum'][:2], self.kwargs['datum'][2:4], self.kwargs['datum'][4:]
        initial_str_for_dates = days + "." + months + "." + years + " 00:00"
        return {
            'start_time': initial_str_for_dates,
            'end_time': initial_str_for_dates,
            'user': self.request.user,
            }

    def get_success_url(self):
        months, years = self.kwargs['datum'][2:4], self.kwargs['datum'][4:]
        first_part_link = reverse('cal:calendar')
        str_for_link = "?month=" + years + "-" + months
        return first_part_link + str_for_link

class EventChoiceListView(LoginRequiredMixin, ListView):
    models          = Event
    template_name   = 'event_choice_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        volba = self.kwargs['choice']
        new_context = Event.objects.filter(type_of_events=volba)
        return new_context
