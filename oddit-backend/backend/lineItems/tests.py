from django.core.handlers import exception
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import LineItem
from events.models import Event

class LineItemModelTests(TestCase):
    name = 'Buy Pizza'
    amount = -25
    category = 1

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='John Doe',
            email='john.doe@testemail.com',
            password='johnyboy',
            club_name="McGill Pizza Pasta Club",
            student_id="27799877",
            user_type=1
        )
        self.event = Event.objects.create(event_name="Java Workshop", event_date="2020-10-19", user=self.user)

    def test_add_line_item_to_existing_event_empty(self):
        line_item = LineItem.objects.create(name=self.name, amount=self.amount, category=self.category, event=self.event)
        self.assertEqual(line_item.name, "Buy Pizza", msg="Line Item has no name!")
        self.assertEqual(line_item.amount, -25, msg="Line Item has no amount!")
        self.assertEqual(line_item.category, 1, msg="Line Item has no category!")
        self.assertEqual(line_item.event, self.event, msg="Line Item has no event!")


    def test_add_line_item_to_existing_event_not_empty(self):
        # Add line item to the event
        LineItem.objects.create(name='Buy Coca Cola', amount=-10, category=1, event=self.event)

        line_item = LineItem.objects.create(name=self.name, amount=self.amount, category=self.category, event=self.event)
        self.assertEqual(line_item.name, "Buy Pizza", msg="Line Item has no name!")
        self.assertEqual(line_item.amount, -25, msg="Line Item has no amount!")
        self.assertEqual(line_item.category, 1, msg="Line Item has no category!")
        self.assertEqual(line_item.event, self.event, msg="Line Item has no event!")

    def test_add_line_item_without_amount(self):
        try:
            LineItem.objects.create(name=self.name, category=self.category, event=self.event)
            self.fail('Can create a line item without amount')
        except IntegrityError:
            pass