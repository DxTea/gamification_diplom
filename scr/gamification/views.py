from .forms import CharacterForm
from .models import Character
from courses.models import Course
from assignments.models import Assignment, SubmittedAssignment
from users.models import CustomUser

from users.decorators import role_required

from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required


def welcome(request):
    return render(request, 'gamification/welcome.html')


@login_required
def deck(request):
    if request.user.role == 'teacher':
        user_courses = Course.objects.filter(teacher=request.user)
    else:
        user_courses = Course.objects.filter(groups=request.user.group)
    courses_info = []
    for course in user_courses:
        unsubmitted_assignments = Assignment.objects.filter(course=course).exclude(
            submittedassignment__student=request.user)
        groups_info = []
        for group in course.groups.all():
            students_info = []
            for student in CustomUser.objects.filter(group=group):
                total_points = course.total_points_earned_by_student(student)
                students_info.append({
                    'student': student,
                    'total_points': total_points,
                })
            groups_info.append({
                'group': group,
                'students_info': students_info,
            })
        total_possible_points = course.total_possible_points()
        courses_info.append({
            'course': course,
            'unsubmitted_assignments': unsubmitted_assignments,
            'groups_info': groups_info,
            'total_possible_points': total_possible_points,
        })
    return render(request, 'gamification/deck.html', {'courses_info': courses_info})


@role_required('student')
def create_character(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            character = form.save(commit=False)
            character.student = request.user
            character.level = 1
            character.experience = 0
            character.save()
            return redirect('users:user_profile', username=request.user.username)
    else:
        form = CharacterForm()
    return render(request, 'gamification/create_character.html', {'form': form})


@role_required('student')
def edit_character(request):
    character = Character.objects.get(student=request.user)
    if request.method == 'POST':
        form = CharacterForm(request.POST, request.FILES, instance=character)
        if form.is_valid():
            form.save()
            return redirect('users:user_profile', username=request.user.username)
    else:
        form = CharacterForm(instance=character)
    return render(request, 'gamification/edit_character.html', {'form': form})


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)


def handler403(request, exception):
    return render(request, 'errors/403.html', status=403)
