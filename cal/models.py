# cal/models.py

from django.db import models
from django.urls import reverse

class Event(models.Model):
    title       = models.CharField(max_length=200)
    #choices for classes in templates
    TYPES = [
    (  "narozeniny","narozeniny"),
    (  "svátek", "svátek"),
    (  "dovolená", "dovolená"),
    (  "doctor", "doctor"),
    (  "other", "other"),
    ]
    
    type_of_events      = models.CharField(max_length=30, choices = TYPES, default="other")
    number_of_repeats   = models.IntegerField(default=1)
    description         = models.TextField(blank=True)
    start_time          = models.DateTimeField()
    end_time            = models.DateTimeField()
    user                = models.ForeignKey('auth.User', on_delete=models.CASCADE)


    @property
    def get_title(self):
        return self.title

    @property
    def get_html_url(self):
        return reverse('cal:event_edit', args=(self.id,))
    @property
    def get_dates_and_times(self):
    	return self.start_time.strftime('%H:%M') + " - " + self.end_time.strftime('%H:%M') 

    @property
    def event_delete(self):
        return reverse('cal:event_delete', args=(self.id,))
    
    @property
    def fetch_class(self):
        dicty = {
            "narozeniny":  'btn btn-primary',
            "svátek":  'btn btn-secondary',
            "dovolená":  'btn btn-success',
            "doctor":  'btn btn-info',
            "other": 'btn btn-warning',
        }
        return dicty[self.type_of_events]
    
    