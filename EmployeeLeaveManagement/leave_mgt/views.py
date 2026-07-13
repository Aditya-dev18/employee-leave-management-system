from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .forms import LeaveStatusForm, EmployeeLeaveForm
from .models import Leave
from .serializers import LeaveSerializer
from employee.models import Employee


def is_hr(user):
    return user.is_authenticated and (
        user.is_superuser or (hasattr(user, "userprofile") and user.userprofile.role == "HR")
    )


def is_employee(user):
    return user.is_authenticated and hasattr(user, "userprofile") and user.userprofile.role == "Employee"


@login_required
@user_passes_test(is_employee, login_url="home")
def apply(request):
    if request.method == "POST":
        form = EmployeeLeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            employee = get_object_or_404(Employee, user=request.user)
            leave.employee = employee
            leave.status = "Pending"
            leave.save()

            return redirect("leave_list")
        
    else: 
        form = EmployeeLeaveForm()

    return render(
        request,
        "leave_mgt/apply.html",
        {"form":form}
    )


@login_required
def list(request):
    leaves = Leave.objects.select_related("employee").all().order_by("-created_at")

    if is_employee(request.user):
        leaves = leaves.filter(employee__user=request.user)

    status_filter = request.GET.get("status", "")
    leave_type_filter = request.GET.get("leave_type", "")

    if status_filter:
        leaves = leaves.filter(status=status_filter)

    if leave_type_filter:
        leaves = leaves.filter(leave_type=leave_type_filter)

    paginator = Paginator(leaves, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "leave_mgt/list.html",
        {
            "leaves": page_obj,
            "status_filter": status_filter,
            "leave_type_filter": leave_type_filter,
        }
    )


@login_required
def update(request, id):
    if is_hr(request.user):
        leave = get_object_or_404(Leave, id=id)
        form_class = LeaveStatusForm
    else:
        leave = get_object_or_404(Leave, id=id, employee__user=request.user, status="Pending")
        form_class = EmployeeLeaveForm

    if request.method == "POST":
        form = form_class(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            return redirect("leave_list")
    else:
        form = form_class(instance=leave)

    return render(request, "leave_mgt/update.html", {"form": form})


@login_required
def delete(request, id):
    if is_hr(request.user):
        leave = get_object_or_404(Leave, id=id)
    else:
        leave = get_object_or_404(Leave, id=id, employee__user=request.user, status="Pending")

    if request.method == "POST":
        leave.delete()
        return redirect("leave_list")

    return render(request, "leave_mgt/delete.html", {"leave": leave})


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def leave_api_list(request):
    if request.method == "GET":
        leaves = Leave.objects.select_related("employee").all().order_by("id")
        if is_employee(request.user):
            leaves = leaves.filter(employee__user=request.user)
        serializer = LeaveSerializer(leaves, many=True)
        return Response(serializer.data)

    data = request.data.copy()
    if is_employee(request.user):
        employee = get_object_or_404(Employee, user=request.user)
        data["employee"] = employee.id
        data["status"] = "Pending"

    serializer = LeaveSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def leave_api_detail(request, id):
    if is_employee(request.user):
        leave = get_object_or_404(Leave, id=id, employee__user=request.user)
    else:
        leave = get_object_or_404(Leave, id=id)

    if request.method == "GET":
        serializer = LeaveSerializer(leave)
        return Response(serializer.data)

    if not is_hr(request.user):
        return Response({"detail": "Only HR can update or delete leave requests through API."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "PUT":
        serializer = LeaveSerializer(leave, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    leave.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

