from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

mobile_validator = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message='Enter a valid 10 digit mobile number.',
)

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("HR", "HR Admin"),
        ("Employee", "Employee"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def clean(self):
        if self.role == "HR":
            hr_exists = UserProfile.objects.filter(role="HR").exclude(id=self.id).exists()
            if hr_exists:
                raise ValidationError("Only one HR admin is allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        self.user.is_staff = self.role == "HR"
        self.user.is_superuser = self.role == "HR"
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10, validators=[mobile_validator])
    joining_date = models.DateField()

    def __str__(self):
        return self.name
