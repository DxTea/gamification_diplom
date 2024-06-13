from django.urls import path, include
from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.courses_list, name='courses_list'),
    path('create/', views.course_create, name='course_create'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('<int:pk>/assignments/', include('assignments.urls', namespace='assignments')),

]
