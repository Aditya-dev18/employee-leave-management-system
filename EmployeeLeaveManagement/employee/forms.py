from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee, UserProfile

class EmployeeForm(forms.ModelForm):
    username = forms.CharField(
        required=False,
        disabled=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Employee
        fields = [
            "employee_id",
            "name",
            "email",
            "department",
            "mobile",
            "joining_date",
        ]
        widgets = {
            "employee_id": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "department": forms.TextInput(attrs={"class": "form-control"}),
            "mobile": forms.TextInput(attrs={"class": "form-control"}),
            "joining_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = getattr(self.instance, "user", None)
        if user:
            self.fields["username"].initial = user.username
        else:
            self.fields.pop("username")

    def save(self, commit=True):
        employee = super().save(commit=commit)
        if commit and employee.user:
            employee.user.email = employee.email
            employee.user.save(update_fields=["email"])
        return employee


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    employee_id = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    department = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    mobile = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    joining_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))

    class Meta:
        model = User
        fields = ["username", "email", "role", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")

        if role == "HR" and (UserProfile.objects.filter(role="HR").exists() or User.objects.filter(is_superuser=True).exists()):
            self.add_error("role", "HR admin already exists. Only one HR admin is allowed.")

        if role == "Employee":
            required_fields = ["employee_id", "name", "department", "mobile", "joining_date"]
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, "This field is required for employee registration.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            role = self.cleaned_data["role"]
            UserProfile.objects.create(user=user, role=role)

            if role == "Employee":
                Employee.objects.create(
                    user=user,
                    employee_id=self.cleaned_data["employee_id"],
                    name=self.cleaned_data["name"],
                    email=self.cleaned_data["email"],
                    department=self.cleaned_data["department"],
                    mobile=self.cleaned_data["mobile"],
                    joining_date=self.cleaned_data["joining_date"],
                )

        return user
