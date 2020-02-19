from django.test import TestCase
from .models import Event
import datetime
from django.contrib.auth import get_user_model
# Create your tests here.

class EventModelTest(TestCase):
	def setUp(self):
		User = get_user_model()
		user = User.objects.create_user(username="karel", email='normal@user.com', password='foo')
		Event.objects.create(title="Zde", start_time=datetime.datetime.now(), end_time=datetime.datetime.now(), user=user)

	def test_event_content(self):
		event = Event.objects.get(id=1)
		expected_title_name = f'{event.title}'
		expected_user_name = f'{event.user}'
		self.assertEqual(expected_title_name, 'Zde')
		self.assertEqual(expected_user_name, 'karel')
		