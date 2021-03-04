from django.core.handlers import exception
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import LineItem
from rest_framework import status
from django.urls import reverse
from events.models import Event
from rest_framework.test import APIClient, APITestCase
import itertools

import uuid

client = APIClient()

LINE_ITEMS_URL = reverse('createLineItem')

class LineItemAPITests(APITestCase):

    line_item_name_1 = 'Buy Pizza'
    line_item_amount_1 = -25
    line_item_category_1 = 1
    line_item_name_2 = 'Ticket Sale'
    line_item_amount_2 = 200
    line_item_category_2 = 2
    line_item_name_3 = 'Soda'
    line_item_amount_3 = -20
    line_item_category_3 = 3


    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='John Doe',
            email='john.doe@testemail.com',
            password='johnyboy',
            club_name="McGill Pizza Pasta Club",
            student_id="27799877",
            user_type=1
        )

        self.event1 = Event.objects.create(event_name="Java Workshop", event_date="2020-10-19", user=self.user)
        self.event2 = Event.objects.create(event_name="Case comp", event_date="2020-11-11", user=self.user)
        self.event3 = Event.objects.create(event_name="Case Challenge", event_date="2020-11-11", user=self.user)
        self.line_item1 = LineItem.objects.create(name="Buy Pop", amount=40, category=1, event=self.event3)
        self.line_item2 = LineItem.objects.create(name="Sell Candy", amount=20, category=1, event=self.event3)

    def initializeDatabaseForQueryTests(self):
        self.client.force_authenticate(self.user)
        data = {"name": self.line_item_name_1, "amount": self.line_item_amount_1, "category": self.line_item_category_1, "event": self.event1.pk}
        self.client.post(LINE_ITEMS_URL, data)
        data = {"name": self.line_item_name_2, "amount": self.line_item_amount_2, "category": self.line_item_category_2, "event": self.event2.pk}
        self.client.post(LINE_ITEMS_URL, data)
        data = {"name": self.line_item_name_3, "amount": self.line_item_amount_3, "category": self.line_item_category_3, "event": self.event2.pk}
        self.client.post(LINE_ITEMS_URL, data)
    

    def test_add_line_item_normal(self):
        self.client.force_authenticate(self.user)
        data = {"name": self.line_item_name_1, "amount": self.line_item_amount_1, "category": self.line_item_category_1, "event": self.event1.pk}
        response = self.client.post(LINE_ITEMS_URL, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 

    # Alternate flow
    def test_add_line_item_alternate(self):
        self.client.force_authenticate(self.user)
        data = {"name": self.line_item_name_2, "amount": self.line_item_amount_2, "category": self.line_item_category_2, "event": self.event1.pk}
        response = self.client.post(LINE_ITEMS_URL, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)         

    # Error flow
    def test_add_line_item_no_name(self):
        self.client.force_authenticate(self.user)
        data = {"amount": self.line_item_amount_1, "category": self.line_item_category_1, "event": self.event1.pk}
        response = self.client.post(LINE_ITEMS_URL, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 

    # Error flow
    def test_add_line_item_no_event(self):
        self.client.force_authenticate(self.user)
        data = {"name": self.line_item_name_2, "amount": self.line_item_amount_2, "category": self.line_item_category_2}
        response = self.client.post(LINE_ITEMS_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#Test cases for ID012_Query_All_Line_Items_Of_An_Event.feature

    # Normal Flow
    def test_query_list_of_line_items(self):
        self.client.force_authenticate(self.user)
        self.initializeDatabaseForQueryTests()
        LINE_ITEMS_BY_EVENT = reverse('queryLineItemByEvent', kwargs={'pk': self.event1.pk})
        response = self.client.get(LINE_ITEMS_BY_EVENT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(*response.data)
        self.assertEqual(data['name'], self.line_item_name_1)
        self.assertEqual(data['amount'], self.line_item_amount_1)
        self.assertEqual(data['category'], self.line_item_category_1)

    # Alternative Flow
    def test_query_list_of_line_items_by_name(self):
        self.client.force_authenticate(self.user)
        self.initializeDatabaseForQueryTests()
        response = self.client.get(LINE_ITEMS_URL, data={'name': self.event2.event_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        data = dict(response.data[0])
        name = data['name']
        if name == self.line_item_name_2:
            self.assertEqual(data['amount'], self.line_item_amount_2)
            self.assertEqual(data['category'], self.line_item_category_2)
            self.assertNotEqual(data['name'], self.line_item_name_1)
            self.assertNotEqual(data['amount'], self.line_item_amount_1)
            self.assertNotEqual(data['category'], self.line_item_category_1)
            data = dict(response.data[1])
            self.assertEqual(data['name'], self.line_item_name_3)
            self.assertEqual(data['amount'], self.line_item_amount_3)
            self.assertEqual(data['category'], self.line_item_category_3)
            self.assertNotEqual(data['name'], self.line_item_name_1)
            self.assertNotEqual(data['amount'], self.line_item_amount_1)
            self.assertNotEqual(data['category'], self.line_item_category_1)
        else:
            self.assertEqual(data['amount'], self.line_item_amount_3)
            self.assertEqual(data['category'], self.line_item_category_3)
            self.assertNotEqual(data['name'], self.line_item_name_1)
            self.assertNotEqual(data['amount'], self.line_item_amount_1)
            self.assertNotEqual(data['category'], self.line_item_category_1)
            data = dict(*response.data[1])
            self.assertEqual(data['name'], self.line_item_name_2)
            self.assertEqual(data['amount'], self.line_item_amount_2)
            self.assertEqual(data['category'], self.line_item_category_2)
            self.assertNotEqual(data['name'], self.line_item_name_1)
            self.assertNotEqual(data['amount'], self.line_item_amount_1)
            self.assertNotEqual(data['category'], self.line_item_category_1)


    # Error Flow
    def test_query_list_of_line_items_incorrect_name(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(LINE_ITEMS_URL + 'wrong_name')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    #ID013 Query Line Items Attribute by ID/Name

    #Normal Flow - Query with ID 
    def test_query_line_item_attribute_by_id(self):
        self.client.force_authenticate(self.user)
        self.initializeDatabaseForQueryTests()
        LINE_ITEMS_BY_ID = reverse('queryLineItemById', kwargs={'pk': self.line_item1.pk})
        response = self.client.get(LINE_ITEMS_BY_ID)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(*response.data)
        self.assertEqual(data['name'], 'Buy Pop')
        self.assertEqual(data['amount'], 40)
        self.assertEqual(data['category'], 1)
    
    #Alternate Flow- Query Attributes by Name


    def test_query_line_item_attribute_by_alternate_id(self):
        self.client.force_authenticate(self.user)
        self.initializeDatabaseForQueryTests()
        LINE_ITEMS_BY_ID = reverse('queryLineItemById', kwargs={'pk': self.line_item2.pk})
        response = self.client.get(LINE_ITEMS_BY_ID)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(*response.data)
        self.assertEqual(data['name'], 'Sell Candy')
        self.assertEqual(data['amount'], 20)
        self.assertEqual(data['category'], 1)
    
    #Error flow - Attributes of line item that does not exist
    def test_query_line_item_attribite_invalid_id(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(LINE_ITEMS_URL + '999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_query_line_item_by_name(self):
        self.client.force_authenticate(self.user)
        data = {"name": self.line_item_name_1, "amount": self.line_item_amount_1, "category": self.line_item_category_1, "event": self.event1.pk}
        response = self.client.post(LINE_ITEMS_URL, data)
        LINE_ITEMS_BY_NAME = reverse('queryLineItemByName', kwargs={'name': self.line_item_name_1})
        response = self.client.get(LINE_ITEMS_BY_NAME)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(*response.data)
        self.assertEqual(data['name'], 'Buy Pizza')
        self.assertEqual(data['amount'], -25)
        self.assertEqual(data['category'], 1)
    
    def test_query_line_item_by_name_2(self):
        self.client.force_authenticate(self.user)
        data = {"name": self.line_item_name_2, "amount": self.line_item_amount_2, "category": self.line_item_category_2, "event": self.event2.pk}
        response = self.client.post(LINE_ITEMS_URL, data)
        LINE_ITEMS_BY_NAME = reverse('queryLineItemByName', kwargs={'name': self.line_item_name_2})
        response = self.client.get(LINE_ITEMS_BY_NAME)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(*response.data)
        self.assertEqual(data['name'], 'Ticket Sale')
        self.assertEqual(data['amount'], 200)
        self.assertEqual(data['category'], 2)

    #Test cases for ID011_Remove_Line_Item_From_Existing_Event.feature

    # Normal flow
    def test_delete_single_line_item_normal(self):
        self.client.force_authenticate(self.user)
        self.initializeDatabaseForQueryTests()
        deletion = reverse('queryLineItemById', kwargs={'pk': self.line_item1.pk})
        response = self.client.delete(deletion)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    # Alternate flow
    def test_delete_multiple_line_items_alternate(self):
        self.client.force_authenticate(self.user)
        self.initializeDatabaseForQueryTests()
        deletion_1 = reverse('queryLineItemById', kwargs={'pk': self.line_item1.pk})
        response = self.client.delete(deletion_1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        deletion_2 = reverse('queryLineItemById', kwargs={'pk': self.line_item2.pk})
        response = self.client.delete(deletion_2)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    # Error flow
    def test_delete_invalid_line_item_error(self):
        self.client.force_authenticate(self.user)
        self.initializeDatabaseForQueryTests()
        deletion = reverse('queryLineItemById', kwargs={'pk': 9999})
        response = self.client.delete(deletion)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
