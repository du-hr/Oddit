from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import EventSerializer
from .models import Event
import datetime


class EventAPIView(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        updated_data = request.data.copy()
        updated_data["user"] = request.user.id
        serializer = self.get_serializer(data=updated_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Event.objects.all()
        end_date = self.request.query_params.get('date', None)
        if end_date is not None:
            # Year, Month, Day format
            date = end_date.split('-')
            queryset = Event.objects.filter(event_date__lt=datetime.date(date[0], date[1], date[2]))
        return queryset  # queryset.order_by('event_date')

    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)


serializer_class = EventSerializer
permission_classes = (IsAuthenticated,)


def parse_date(date):
    if date is None:
        return date
    date = date.split('-')
    return datetime.date(int(date[0]), int(date[1]), int(date[2]))


@api_view(['GET'])
def api_query_events(request):
    queryset = Event.objects.all()
    try:
        start_date = parse_date(request.query_params.get('start_date'))
        end_date = parse_date(request.query_params.get('end_date'))
    except (ValueError, IndexError):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            "message": "Dates must be formatted as yyyy-mm-dd"
        })

    if start_date is not None:
        queryset = queryset.filter(event_date__gte=start_date)
    if end_date is not None:
        queryset = queryset.filter(event_date__lte=end_date)

    return Response(EventSerializer(queryset, many=True).data)


@api_view(['DELETE'])
def api_delete_event_view(request, ids):
    try:
        event_to_delete = Event.objects.filter(pk=ids)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        event_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def api_update_event_view(request, ids):
    try:
        event_to_update = Event.objects.get(pk=ids)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    event_serializer = EventSerializer(event_to_update, data=request.data)
    if request.method == 'PUT':
        if event_serializer.is_valid():
            event_serializer.save()
            return Response(event_serializer.data)

    return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
