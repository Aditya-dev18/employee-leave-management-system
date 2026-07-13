from django import forms
from .models import Leave

class LeaveForm(forms.ModelForm):

    class Meta: 
        model = Leave
        fields = [
            "employee",
            "leave_type",
            "from_date",
            "to_date",
            "reason",
        ]
        widgets = {
            "employee": forms.Select(attrs={"class": "form-select"}),
            "leave_type": forms.Select(attrs={"class": "form-select"}),
            "from_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "to_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")

        if from_date and to_date:
            if from_date > to_date:
                 self.add_error("from_date", "From Date Cannot be greater than To Date.")
        return cleaned_data


class LeaveStatusForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class EmployeeLeaveForm(LeaveForm):
    class Meta(LeaveForm.Meta):
        fields = [
            "leave_type",
            "from_date",
            "to_date",
            "reason",
        ]
        widgets = {
            "leave_type": forms.Select(attrs={"class": "form-select"}),
            "from_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "to_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
