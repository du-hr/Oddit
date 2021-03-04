from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Event
import json

import uuid

EVENTS_URL = reverse('createEvent')
client = APIClient()


def event_to_list(e):
    return e.event_id, e.event_name, e.event_date, e.user


class EventAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='Jon Doe',
            email='medo@testemail.com',
            password='thispasswordisbad',
            club_name="McGill Tennis Club",
            student_id="27799877",
            user_type=1,
        )
        self.client.force_authenticate(self.user)
        self.events = []
        self.events.append(Event.objects.create(event_name="Test Event1", event_date="2020-01-30", user=self.user))
        self.getResponse = self.client.get(EVENTS_URL)
        self.events.append(Event.objects.create(event_name="Test Event2", event_date="2020-03-30", user=self.user))
        self.events.append(Event.objects.create(event_name="Test Event3", event_date="2020-05-30", user=self.user))

    def assertResponseRepresentsEvent(self, resp, event):
        self.assertEqual(resp["event_name"], event.event_name)
        self.assertEqual(resp["event_date"], event.event_date)
        self.assertEqual(resp["event_id"], str(event.event_id))
        self.assertEqual(resp["user"], event.user.id)

    def test_create_event_normal(self):
        data = {"user": self.user.id, "event_name": "New Test Event", "event_date": "2020-09-30"}
        response = self.client.post(EVENTS_URL, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_not_login(self):
        self.client.logout()
        data = {"event_name": "Test Event", "event_date": "2020-09-30"}
        response = self.client.post(EVENTS_URL, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # The Following Tests are exclusively for the event delete feature

    def test_query_all_events(self):
        response = self.client.get(EVENTS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.events))
        for r, e in zip(response.data, self.events):
            self.assertResponseRepresentsEvent(r, e)

    def test_query_events_two_dates(self):
        data = {
            "start_date": "2020-03-22",
            "end_date": "2020-10-01"
        }
        response = self.client.get(reverse('queryByDate'), data=data)
        events_dates = [self.events[1].event_date, self.events[2].event_date]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(json.dumps(response.data))
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0].get('event_date'), events_dates[0])
        self.assertEqual(content[1].get('event_date'), events_dates[1])

    def test_query_events_both_dates_null(self):
        response = self.client.get(reverse('queryByDate'), data={})
        events_dates = [e.event_date for e in self.events]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(json.dumps(response.data))
        self.assertEqual(len(content), 3)
        self.assertEqual(content[0].get('event_date'), events_dates[0])
        self.assertEqual(content[1].get('event_date'), events_dates[1])
        self.assertEqual(content[2].get('event_date'), events_dates[2])

    def test_query_events_start_date_only(self):
        data = {
            "start_date": "2020-04-22"
        }
        response = self.client.get(reverse('queryByDate'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(json.dumps(response.data))
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0].get('event_date'), '2020-05-30')

    def test_query_events_end_date_only(self):
        data = {
            "end_date": "2020-03-01"
        }
        response = self.client.get(reverse('queryByDate'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(json.dumps(response.data))
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0].get('event_date'), '2020-01-30')

    def test_query_events_invalid_format(self):
        data = {
            "start_date": "not a date"
        }
        response = self.client.get(reverse('queryByDate'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Dates must be formatted as yyyy-mm-dd')

    # The following tests are exclusively for the event delete feature.

    def test_delete_single_event(self):
        event_1 = Event.objects.create(event_name="Test Event1", event_date="2020-09-30", user=self.user)
        response = self.client.delete(reverse('delete', kwargs={'ids': event_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_multiple_events(self):
        # event_1 = Event.objects.create(event_name="Test Event1", event_date="2020-09-30", user=test_user)
        event_2 = Event.objects.create(event_name="Test Event2", event_date="2020-09-30", user=self.user)
        event_3 = Event.objects.create(event_name="Test Event3", event_date="2020-09-30", user=self.user)
        # uuidlist = [event_2.pk, event_3.pk]
        # events_pks = ",".join((event2_pkString, event3_pkString))
        response = self.client.delete(reverse('delete', kwargs={'ids': event_2.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(reverse('delete', kwargs={'ids': event_3.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_event(self):
        response = self.client.delete(
            reverse('delete', kwargs={'ids': uuid.UUID('193a88cc-2b78-4ddc-9ef8-632cde33ef74')}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Testing Get and then 3 flows of query attributes of an event
    def test_get(self):
        self.assertEqual(self.getResponse.status_code, status.HTTP_200_OK)

    def test_attribute_of_an_event_by_name(self):
        od = self.getResponse.data[0]
        items = list(od.items())
        self.assertEqual(items[1], ('event_name', 'Test Event1'))
        self.assertEqual(items[2], ('event_date', '2020-01-30'))

    def test_attribute_of_an_event_by_date(self):
        od = self.getResponse.data[0]
        items = list(od.items())
        self.assertEqual(items[1], ('event_name', 'Test Event1'))
        self.assertEqual(items[2], ('event_date', '2020-01-30'))

    def test_attribute_of_an_event_by_id_normal(self):
        i = str(self.events[0].event_id)
        od = self.getResponse.data[0]
        items = list(od.items())
        self.assertEqual(items[0], ('event_id', i))
        self.assertEqual(items[1], ('event_name', 'Test Event1'))
        self.assertEqual(items[2], ('event_date', '2020-01-30'))

    def test_delete_an_attribute_of_an_event(self):
        event_1 = Event.objects.create(event_name="Test Event1", event_date="2020-09-30", user=self.user)
        response = self.client.delete(reverse('delete', kwargs={'ids': event_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test cases for ID009_Update_Event_Attributes.feature
    # ID009_Update_Event_Attributes.feature (Normal Flow)
    def test_update_event_name_and_date(self):
        response = self.client.put(
            reverse('updateEvent', kwargs={'ids': self.events[0].pk}),
            data={"user": self.user.id, "event_name": "New Event", "event_date": "2020-10-30"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = list(response.data.items())
        self.assertEqual(items[1], ('event_name', 'New Event'))
        self.assertEqual(items[2], ('event_date', '2020-10-30'))

    # ID009_Update_Event_Attributes.feature (Alternative Flow)
    def test_update_event_name(self):
        response = self.client.put(
            reverse('updateEvent', kwargs={'ids': self.events[0].pk}),
            data={"user": self.user.id, "event_name": "New Event", "event_date": "2020-09-30"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = list(response.data.items())
        self.assertEqual(items[1], ('event_name', 'New Event'))

    # ID009_Update_Event_Attributes.feature (Error Flow)
    def test_update_event_false_ID(self):
        response = self.client.put(
            reverse('updateEvent', kwargs={'ids': uuid.UUID('193a88cc-2b78-4ddc-9ef8-632cde33ef74')}),
            data={"user": self.user.id, "event_name": "New Event", "event_date": "2020-09-30"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ID009_Update_Event_Attributes.feature (Error Flow)
    def test_update_event_user_not_log_in(self):
        self.client.logout()
        response = self.client.put(
            reverse('updateEvent', kwargs={'ids': self.events[0].pk}),
            data={"user": self.user.id, "event_name": "New Event", "event_date": "2020-09-30"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
