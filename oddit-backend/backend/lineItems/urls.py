
from django.urls import path  
from django.contrib import admin
from .views import ListItemAPIView, ListItemAPIViewByEvent, ListItemAPIViewById, queryLineItemByName

"""
Info:
https://stackoverflow.com/questions/32876275/how-to-filter-for-multiple-ids-from-a-query-param-on-a-get-request-with-django-r
https://stackoverflow.com/questions/32950432/django-urls-uuid-not-working
"""
urlpatterns = [

    path('', ListItemAPIView.as_view(), name='createLineItem'),
    path('queryName/<str:name>/', queryLineItemByName.as_view(), name='queryLineItemByName'),
    path('<uuid:pk>/', ListItemAPIViewByEvent.as_view(), name='queryLineItemByEvent'),
    path('queryId/<int:pk>/', ListItemAPIViewById.as_view(), name='queryLineItemById'),

]