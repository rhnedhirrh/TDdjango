from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

#----------------------------------------------------------------------
from django.core.exceptions import ValidationError
import re
def validate_letters_only(value):
    if not re.match(r'^[A-Za-z\s]+$',value):
        raise ValidationError('This field should contain only letters')
#----------------------------------------------------------------------



class Category(models.Model):
    letters_only=RegexValidator(r'^[A-Za-z\s]+$','only letters are allowed')
    #title=models.CharField(max_length=255,unique=True,validators=[letters_only])
    title=models.CharField(max_length=255,unique=True,validators=[validate_letters_only])
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural='Categories'
