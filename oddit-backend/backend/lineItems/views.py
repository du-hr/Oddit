from django.shortcuts import render
from rest_framework import status, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import LineItemSerializer
from events.models import Event
from .models import LineItem
import datetime

class ListItemAPIView(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = LineItem.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(event__event_name=name)
        return queryset
    serializer_class = LineItemSerializer
    permission_classes = (IsAuthenticated,)


class ListItemAPIViewByEvent(generics.ListCreateAPIView):
    def get_queryset(self):
        event_id = self.kwargs["pk"]
        return LineItem.objects.filter(event_id=event_id)
    serializer_class = LineItemSerializer
    permission_classes = (IsAuthenticated,)

class ListItemAPIViewById(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    def get_queryset(self):
        lineItem_id = self.kwargs["pk"]
        return LineItem.objects.filter(id=lineItem_id)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    serializer_class = LineItemSerializer
    permission_classes = (IsAuthenticated,)

class queryLineItemByName(generics.ListCreateAPIView):
    def get_queryset(self):
        lineItem_Name = self.kwargs["name"]
        return LineItem.objects.filter(name=lineItem_Name)
    serializer_class = LineItemSerializer
    permission_classes = (IsAuthenticated,)