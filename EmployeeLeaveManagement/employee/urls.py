from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("register/", views.register, name="register"),
    path('add/', views.add, name="add"),
    path("list/", views.list, name="employee_list"),
    path("profile/", views.profile, name="profile"),
    path("update/<int:id>/",views.update,name="update_employee"),
    path("delete/<int:id>/", views.delete, name="delete_employee"),
    path("api/employees/", views.employee_api_list, name="employee_api_list"),
    path("api/employees/<int:id>/", views.employee_api_detail, name="employee_api_detail"),
]
