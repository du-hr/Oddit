from django.urls import path
from django.contrib import admin
from .views import EventAPIView, api_update_event_view
from .views import api_delete_event_view
from .views import api_query_events

"""
An example of event delete shall be:
1. Delete One event
events/delete/b9caf199-26c2-4027-b39f-5d0693421506

OR:
2. Delete Multiple events
events/?ids=b9caf199-26c2-4027-b39f-5d0693421506,20000009-26c2-4027-b39f-5d0693421506

*Put ONLY ONE comma in between uuids to send.

Info:
https://stackoverflow.com/questions/32876275/how-to-filter-for-multiple-ids-from-a-query-param-on-a-get-request-with-django-r
https://stackoverflow.com/questions/32950432/django-urls-uuid-not-working
"""
urlpatterns = [

    path('', EventAPIView.as_view(), name='createEvent'),
    path('dateRange/', api_query_events, name='queryByDate'),
    path('<uuid:ids>/', api_delete_event_view, name='delete'),
    path('update/<uuid:ids>/', api_update_event_view, name='updateEvent'),

]
