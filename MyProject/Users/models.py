from django.db import models
from django.contrib.auth.models import AbstractUser
from Conferences.models import Conference
from django.core.validators import RegexValidator
from django.utils import timezone
# Create your models here.
from django.core.exceptions import ValidationError

def email_validator(value):
    if not value.endswith('@esprit.tn'):
        raise ValidationError('Email invalid')

class Participant(AbstractUser):
    cin_validators=RegexValidator(
        regex=r'^\d{8}$',
        message="This Field must contain exactly 8 digits"
    )
    cin=models.CharField(max_length=8,primary_key=True,validators=[cin_validators])
    
    CHOICES=[
        ('etudiant','etudiant'),
        ('enseignant','enseignant'),
        ('docteur','docteur'),
        ('chercheur','chercheur')
    ]
    participant_category=models.CharField(max_length=255,choices=CHOICES)
   
    email=models.EmailField(unique=True,max_length=255,validators=[email_validator])

    # Utiliser l'email pour l'authentification
    username=models.CharField(max_length=255,unique=True)
    USERNAME_FIELD = 'username'

    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    

    Reservations=models.ManyToManyField(Conference,through='Reservation',related_name='Reservations')
    #related_name='Reservations': This defines how you will access the Reservations from the Conference model.
    # cat Conferences.all()


    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural='Participants'

        
class Reservation(models.Model):
    confirmed=models.BooleanField(default=False)
    reservation_date=models.DateTimeField(auto_now_add=True)

    conference=models.ForeignKey(Conference,on_delete=models.CASCADE)
    participant=models.ForeignKey(Participant,on_delete=models.CASCADE)

#reservation_date : la réservation ne peut être faite que pour des conférences à venir (Enutilisant la fonction clean).

    def clean(self):
        if self.conference.start_date < timezone.now().date() : 
            raise ValidationError("You can only reserve for upcoming")
#------------------------------------------------------------------------------------------------mafhmthech------------
        reservation_count=Reservation.objects.filter(
            participant = self.participant,
            reservation_date = self.reservation_date
        )
        if reservation_count >= 3 :
            raise ValidationError("You can only make up to 3 reservations")
    class Meta :
        unique_together=('conference','participant')
        verbose_name_plural='Réservations'