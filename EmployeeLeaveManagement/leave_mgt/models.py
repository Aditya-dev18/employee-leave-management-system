from django.db import models
from employee.models import Employee
from django.core.exceptions import ValidationError

LEAVE_TYPE_CHOICES = [
    ("Casual", "Casual"),
    ("Sick", "Sick"),
    ("Earned", "Earned"),
]

STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Rejected", "Rejected"),
]


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.from_date > self.to_date:

            raise ValidationError("From Date cannot be greater than To Date")

    def __str__(self):
        return f"{self.employee.name} - {self.leave_type}"
