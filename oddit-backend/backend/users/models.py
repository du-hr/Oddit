from django.contrib.auth.models import AbstractUser 
from django.db import models

class CustomUser(AbstractUser):

    club_name = models.CharField(max_length = 70)
    student_id = models.CharField(max_length= 10)
    USER_TYPE_CHOICES = (
      (1, 'Treasurer'),
      (2, 'President')
    )


    user_type = models.PositiveSmallIntegerField(choices = USER_TYPE_CHOICES, null= True)

    REQUIRED_FIELDS = ['club_name', 'student_id', 'user_type']

    #not sure if have to create a function that returns by displaying the results 
    #but created a string representation for testing
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.student_id} {self.club_name} {self.user_type}"
