# cal/utils.py

from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event


class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(start_time__day=day)
		d = f'{self.get_link(day, self.month, self.year)}'
		for event in events_per_day:
			#přidat podmínku na multidny
		   d += f' <a class="{event.fetch_class}" href="{event.get_html_url}"> <object><a href="{event.event_delete}" class="badge badge-danger"> &#128465; </a></object>  <br> {event.get_title} <h6><br> {event.get_dates_and_times} </h6></a>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'<tr><td colspan=7 align="center"><p class="h4">{self.year}  -  '
		cal += f'{self.translate_months(month=self.month) }</p></td></tr>\n'
		cal += f'<tr class="table-active"><td>Po</td><td>Út</td><td>St</td><td>Čt</td><td>Pá</td><td>So</td><td>Ne</td></tr> \n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal

	def translate_months(self,month=None, year=None):
		months = {1: 'Leden', 2: "Únor", 3: 'Březen',4: 'Duben', 5: "Květen", 6: 'Červen', 
		7: 'Červenec', 8: "Srpen", 9: 'Září', 10: 'Říjen', 11: 'Listopad', 12: 'Prosinec'}
		return months[month]


	def get_link(self, day, month, year):
		day_link, month_link, year_link = str(day), str(month), str(year)
		if len(day_link) == 1:
			day_link = "0" + str(day_link)
		if len(month_link) == 1:
			month_link = "0" + str(month_link)
		if len(year_link) == 1:
			year_link = "0" + str(year_link)
		final_string_for_address = day_link + month_link + year_link
		return f"<a class='btn btn-light' href ='./event/new/{final_string_for_address}'>&#128204;</a><br><br>" 