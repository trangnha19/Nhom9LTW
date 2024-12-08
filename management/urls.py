from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='management'),
    path('employee/', views.employee, name='employee'),
    path('employee/create/', views.create_employee, name='create-employee'),
    path('employee/update/<str:username>/', views.update_employee, name='create-employee'),
    path('sheet/', views.main_sheet, name='main-sheet'),
    path('salary/', views.total_salary, name='total-salary'),
    path('letter/', views.letter, name='main-letter'),
    path('dayoff/', views.admin_review_requests, name='dayoff'),
]
