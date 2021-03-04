from django.core.handlers import exception
from django.db import IntegrityError
from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Event


class ModelTests(TestCase):
    email = 'medo@testemail.com'
    password = 'thispasswordisbad'
    username = 'Jon Doe'
    club_name = "McGill Tennis Club"
    student_id = "27799877"
    user_type = 1

    def test_create_event_successful(self):
        test_user = get_user_model().objects.create_user(
            username=ModelTests.username,
            email=ModelTests.email,
            password=ModelTests.password,
            club_name=ModelTests.club_name,
            student_id=ModelTests.student_id,
            user_type=ModelTests.user_type,
        )
        event = Event(event_name="Test Event", event_date="2020-09-30", user=test_user)
        event.save()
        self.assertEqual(event.event_name, "Test Event")
        self.assertEqual(event.event_date, "2020-09-30")
        self.assertEqual(event.user, test_user)

    def test_create_event_no_name(self):
        test_user = get_user_model().objects.create_user(
            username=ModelTests.username,
            email=ModelTests.email,
            password=ModelTests.password,
            club_name=ModelTests.club_name,
            student_id=ModelTests.student_id,
            user_type=ModelTests.user_type,
        )

        event = Event(event_date="2020-09-30", user=test_user)
        # NOT so sure if this matches our feature file
        event.save()
        self.assertEqual(event.event_name, "", msg="Event has no name!")

    def test_create_event_no_date(self):
        test_user = get_user_model().objects.create_user(
            username=ModelTests.username,
            email=ModelTests.email,
            password=ModelTests.password,
            club_name=ModelTests.club_name,
            student_id=ModelTests.student_id,
            user_type=ModelTests.user_type,
        )

        event = Event(event_name="Test Event", user=test_user)
        try:
            event.save()
            self.fail("No date!")
        except IntegrityError:
            pass

    def test_create_event_no_user(self):
        # not sure if it should be an API test
        event = Event(event_name="Test Event", event_date="2020-09-30")
        try:
            event.save()
            self.fail("No user!")
        except IntegrityError:
            pass

    def test_create_duplicated_event(self):
        test_user = get_user_model().objects.create_user(
            username=ModelTests.username,
            email=ModelTests.email,
            password=ModelTests.password,
            club_name=ModelTests.club_name,
            student_id=ModelTests.student_id,
            user_type=ModelTests.user_type,
        )
        event = Event(event_name="Test Event", event_date="2020-09-30", user=test_user)
        event.save()
        event_copy = Event(event_name="Test Event", event_date="2020-09-30", user=test_user)
        try:
            event_copy.save()
            self.fail("Event duplication!")
        except IntegrityError:
            pass
    


