from django.db import models
from Categories.models import Category
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.

class Conference(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField(max_length=255)
    start_date=models.DateField(default=timezone.now().date())
    end_date=models.DateField()
    location=models.CharField(max_length=255)
    price=models.FloatField()
    capacity=models.IntegerField(validators=[MaxValueValidator(limit_value=100,message="Capacity must be under 100")])
    program=models.FileField(upload_to='files/',validators=[FileExtensionValidator(allowed_extensions=['pdf','png','jpg','jpeg'],message="Only pdf, pnf, jpg, jpeg")])

    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="Conferences")


    def clean(self):
        if self.end_date <= self.start_date : 
            raise ValidationError("End Date must be after start Date")



    class Meta:
        verbose_name_plural='Conférences'
        constraints=[
            models.CheckConstraint(
                check=models.Q(
                    start_date__gte = timezone.now().date()
                ),
                name="The start date must be greater or equal than today"

            )
        ]