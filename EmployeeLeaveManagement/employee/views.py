from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .forms import EmployeeForm, RegisterForm
from .models import Employee, UserProfile
from .serializers import EmployeeSerializer
from leave_mgt.models import Leave


def is_hr(user):
    return user.is_authenticated and (
        user.is_superuser or (hasattr(user, "userprofile") and user.userprofile.role == "HR")
    )


def is_employee(user):
    return user.is_authenticated and hasattr(user, "userprofile") and user.userprofile.role == "Employee"


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def home(request):
    leaves = Leave.objects.select_related("employee").all()
    query = request.GET.get("q", "")

    if is_employee(request.user):
        leaves = leaves.filter(employee__user=request.user)
    elif query:
        leaves = leaves.filter(
            Q(employee__employee_id__icontains=query) |
            Q(employee__name__icontains=query) |
            Q(employee__email__icontains=query) |
            Q(employee__department__icontains=query) |
            Q(employee__mobile__icontains=query) |
            Q(employee__joining_date__icontains=query) |
            Q(employee__user__username__icontains=query) |
            Q(leave_type__icontains=query) |
            Q(from_date__icontains=query) |
            Q(to_date__icontains=query) |
            Q(reason__icontains=query) |
            Q(status__icontains=query)
        )

    total_employees = Employee.objects.count() if is_hr(request.user) else 1
    total_leaves = leaves.count()
    pending_leaves = leaves.filter(status="Pending").count()
    approved_leaves = leaves.filter(status="Approved").count()
    rejected_leaves = leaves.filter(status="Rejected").count()
    recent_leaves = leaves.order_by("-created_at")[:5]

    return render(
        request,
        "employee/home.html",
        {
            "total_employees": total_employees,
            "total_leaves": total_leaves,
            "pending_leaves": pending_leaves,
            "approved_leaves": approved_leaves,
            "rejected_leaves": rejected_leaves,
            "recent_leaves": recent_leaves,
            "query": query,
        },
    )


@login_required
@user_passes_test(is_hr, login_url="home")
def add(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("employee_list")
        
    else: 
        form = EmployeeForm()

    return render(request,
                  "employee/add.html",
                  {"form": form}
                  )


@login_required
@user_passes_test(is_hr, login_url="home")
def list(request):
    query = request.GET.get("q", "")
    employees = Employee.objects.all().order_by("name")

    if query:
        employees = employees.filter(
            Q(employee_id__icontains=query) |
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(department__icontains=query) |
            Q(mobile__icontains=query) |
            Q(joining_date__icontains=query) |
            Q(user__username__icontains=query)
        )

    paginator = Paginator(employees, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "employee/list.html",
        {"employees": page_obj, "query": query}
    )


@login_required
@user_passes_test(is_hr, login_url="home")
def update(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)

        if form.is_valid():
            form.save()

            return redirect("employee_list")
        
    else:
        form = EmployeeForm(instance=employee)

    return render(
        request,
        "employee/update.html",
        {"form": form, "back_url": "employee_list", "title": "Update Employee"}
    )


@login_required
@user_passes_test(is_employee, login_url="home")
def profile(request):
    employee = get_object_or_404(Employee, user=request.user)

    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = EmployeeForm(instance=employee)

    return render(
        request,
        "employee/update.html",
        {"form": form, "back_url": "home", "title": "My Profile"}
    )


@login_required
@user_passes_test(is_hr, login_url="home")
def delete(request, id):
    employee = get_object_or_404(Employee, id = id)

    if request.method == "POST":
        employee.delete()

        return redirect('employee_list')
    
    return render(
        request,
        "employee/delete.html",
        {"employee": employee}
    )


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def employee_api_list(request):
    if not is_hr(request.user):
        return Response({"detail": "Only HR can access employee API."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        employees = Employee.objects.all().order_by("id")
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def employee_api_detail(request, id):
    if not is_hr(request.user):
        return Response({"detail": "Only HR can access employee API."}, status=status.HTTP_403_FORBIDDEN)

    employee = get_object_or_404(Employee, id=id)

    if request.method == "GET":
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    employee.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
