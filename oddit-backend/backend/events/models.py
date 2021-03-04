from django.db import models

# Create your models here.
import uuid
from django.contrib.auth import get_user_model
from django.db import models


class Event(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=30)
    event_date = models.DateField('Date of the event.')
    # Many (events)-to-one (user) relationships
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        unique_together = ('event_name', 'event_date', 'user')
