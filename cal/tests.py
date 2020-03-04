from django.test import TestCase, SimpleTestCase, Client
from .models import Event
import datetime
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.

def login(client):
	'''Helper function - login.'''
	credentials = {
			'username': "karel",
			'password': "foo",
		}
	return client.post('/accounts/login/', credentials, follow=True)

def setup_user():
	'''Helper function - user creation'''
	User = get_user_model()
	user = User.objects.create_user(username="karel", email='normal@user.com', password='foo')
	return user

def stringed_date():
	'''Helper function - stringify today´s date'''
	if datetime.date.today().month < 10:
			stringed_month = "0" + str(datetime.date.today().month)
	else:
		stringed_month = str(datetime.date.today().month)
	stringed_date = str(datetime.date.today().day) + stringed_month + str(datetime.date.today().year)
	return stringed_date

def create_event_object(user):
	return Event.objects.create(title="Zde", start_time=datetime.datetime.now(), end_time=datetime.datetime.now(), user=user)

class EventModelTest(TestCase):
	def setUp(self):
		user = setup_user()
		create_event_object(user)

	def test_event_content(self):
		event = Event.objects.get(id=1)
		expected_title_name = f'{event.title}'
		expected_user_name = f'{event.user}'
		self.assertEqual(expected_title_name, 'Zde')
		self.assertEqual(expected_user_name, 'karel')
		
class LoginTest(TestCase):
	def setUp(self):
		setup_user()

	def test_login(self):
		response = login(self.client)
		self.assertTrue(response.context['user'].is_active)

class CalendarViewTests(TestCase):
	def setUp(self):
		setup_user()
		login(self.client)

	def test_calendar_status_code(self):
		response = self.client.get('/calendar/')
		self.assertEqual(response.status_code, 200)

	def test_view_url_by_name(self):
		response = self.client.get(reverse('cal:calendar'))
		self.assertEqual(response.status_code, 200)

	def test_view_uses_correct_template(self):
		response = self.client.get(reverse('cal:calendar'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'calendar.html')

class EventNewViewTest(TestCase):
	def setUp(self):
		user = setup_user()
		create_event_object(user)
		login(self.client)

	def test_event_new_exists_proper_url(self):
		response = self.client.get('/event/new/')
		self.assertEqual(response.status_code, 200)

	def test_event_new_url_by_name(self):
		response = self.client.get(reverse('cal:event_new'))
		self.assertEqual(response.status_code, 200)

	def test_event_new_uses_correct_template(self):
		response = self.client.get(reverse('cal:event_new'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'event.html')

class EventNewFromCalViewTest(TestCase):
	def setUp(self):
		user = setup_user()
		create_event_object(user)
		login(self.client)

	def test_event_new_exists_proper_url(self):
		stringified_date = stringed_date()
		response = self.client.get('/calendar/event/new/' + stringified_date + '/')
		self.assertEqual(response.status_code, 200)

	def test_event_new_url_by_name(self):
		datum = stringed_date()
		response = self.client.get(reverse('cal:new_event_from_cal', kwargs={'datum': datum}), follow=True)
		self.assertEqual(response.status_code, 200)

	def test_event_new_uses_correct_template(self):
		datum = stringed_date()
		response = self.client.get(reverse('cal:new_event_from_cal', kwargs={'datum': datum}), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'event.html')

class EventEditViewTest(TestCase):
	def setUp(self):
		user = setup_user()
		create_event_object(user)
		login(self.client)

	def test_event_detail_exists_proper_url(self):
		response = self.client.get('/event/edit/1/')
		self.assertEqual(response.status_code, 200)

	def test_event_detail_url_by_name(self):
		response = self.client.get(reverse('cal:event_edit', args=(1,)), follow=True)
		self.assertEqual(response.status_code, 200)

	def test_event_detail_uses_correct_template(self):
		response = self.client.get(reverse('cal:event_edit',args=(1,)), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'event.html')

class EventDeleteViewTest(TestCase):
	def setUp(self):
		user = setup_user()
		create_event_object(user)
		login(self.client)

	def test_event_delete(self):
		post_response = self.client.post(reverse('cal:event_delete', args=(1,)), follow=True)
		self.assertRedirects(post_response, '/calendar/?month=2020-03', status_code=302)
		self.assertFalse(Event.objects.filter(pk=1).exists())

class EventChoiceListViewTest(TestCase):
	def setUp(self):
		user = setup_user()
		create_event_object(user)
		login(self.client)

	def test_list_event_exists_proper_url(self):
		response = self.client.get('/list_events/other/')
		self.assertEqual(response.status_code, 200)

	def test_list_event_url_by_name(self):
		response = self.client.get(reverse('cal:event_choice_list', kwargs={'choice': 'other'}), follow=True)
		self.assertEqual(response.status_code, 200)

	def test_list_event_uses_correct_template(self):
		response = self.client.get(reverse('cal:event_choice_list', kwargs={'choice': 'other'}), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'event_choice_list.html')

class EventComingListViewTest(TestCase):
	def setUp(self):
		user = setup_user()
		create_event_object(user)
		login(self.client)

	def test_list_event_exists_proper_url(self):
		response = self.client.get('/event_coming_list/')
		self.assertEqual(response.status_code, 200)

	def test_list_event_url_by_name(self):
		response = self.client.get(reverse('cal:event_coming_list'))
		self.assertEqual(response.status_code, 200)

	def test_list_event_uses_correct_template(self):
		response = self.client.get(reverse('cal:event_coming_list'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'event_coming_list.html')