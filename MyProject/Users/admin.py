from django.contrib import admin
from .models import Participant
from .models import Reservation


# Register your models here.

admin.site.register(Participant)
admin.site.register(Reservation)
