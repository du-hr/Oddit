from django.db import models
from django.contrib.auth import get_user_model
from events.models import Event

class LineItem(models.Model):
    # ID is autounique field by default
    name = models.CharField(max_length=30)
    amount = models.IntegerField()

    class LineItemCategory(models.IntegerChoices):
        FOOD = 1
        RECREATION = 2
        TV = 3
        SPONSORSHIP = 4

    category = models.IntegerField(choices=LineItemCategory.choices, null=True)
    # Many (events)-to-one (user) relationships
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return '%s, %s' % (self.name, self.event.event_name)