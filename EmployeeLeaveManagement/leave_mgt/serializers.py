from rest_framework import serializers
from .models import Leave


class LeaveSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.name", read_only=True)

    class Meta:
        model = Leave
        fields = [
            "id",
            "employee",
            "employee_name",
            "leave_type",
            "from_date",
            "to_date",
            "reason",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        from_date = data.get("from_date", getattr(self.instance, "from_date", None))
        to_date = data.get("to_date", getattr(self.instance, "to_date", None))

        if from_date and to_date and from_date > to_date:
            raise serializers.ValidationError("From Date cannot be greater than To Date.")

        return data
