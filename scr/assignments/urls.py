from django.urls import path
from . import views

app_name = 'assignments'
urlpatterns = [
    path('<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('create/', views.assignment_create, name='assignment_create'),
    path('<int:pk>/delete/', views.assignment_delete, name='assignment_delete'),
    path('<int:pk>/edit/', views.assignment_edit, name='assignment_edit'),
    path('download/<path:path>', views.download, name='download'),
    path('review/<int:course_id>/', views.review_assignments, name='review_assignments'),
    path('grade/<int:pk>/', views.grade_assignment, name='grade_assignment'),
]
