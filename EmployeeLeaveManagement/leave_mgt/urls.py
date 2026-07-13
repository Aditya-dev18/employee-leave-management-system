from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.apply, name="apply_leave"),
    path('leave-list/', views.list, name="leave_list"),
    path("leave-update/<int:id>/", views.update, name="update_leave"),
    path("leave-delete/<int:id>/", views.delete, name="delete_leave"),
    path("api/leaves/", views.leave_api_list, name="leave_api_list"),
    path("api/leaves/<int:id>/", views.leave_api_detail, name="leave_api_detail"),
]
