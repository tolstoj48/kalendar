# cal/models.py

from django.db import models
from django.urls import reverse

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}" class="badge badge-danger"> {self.title} </a>'

    @property
    def get_dates_and_times(self):
    	return self.start_time.strftime('%H:%M') + " - " + self.end_time.strftime('%H:%M') 

    @property
    def event_delete(self):
        url = reverse('cal:event_delete', args=(self.id,))
        return  f'<a href="{url}" class="badge badge-danger"> X </a>'
    
    