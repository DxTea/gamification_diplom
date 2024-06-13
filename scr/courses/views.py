from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from .forms import CourseForm
from gamification.models import CourseCharacter

from users.decorators import role_required

from django.contrib.auth.decorators import login_required


@login_required
def courses_list(request):
    if request.user.role == 'teacher':
        courses = Course.objects.filter(teacher=request.user)
    else:
        courses = Course.objects.filter(
            groups=request.user.group)
    return render(request, 'courses/courses_list.html', {'courses': courses})


@role_required('teacher')
def course_create(request):
    if not request.user.role == 'teacher':
        return redirect('courses:courses_list')
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            form.save_m2m()
            return redirect('courses:courses_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_create.html', {'form': form})


@role_required('teacher')
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if not request.user == course.teacher:
        return redirect('courses:courses_list')
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            form.save_m2m()
            return redirect('courses:course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_edit.html', {'form': form})


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.role == 'student':
        total_points = course.total_possible_points()
        earned_points = course.total_points_earned_by_student(request.user)
        progress = int(round((earned_points / total_points) * 100, 0)) if total_points else 0
        course_character, created = CourseCharacter.objects.get_or_create(
            character=request.user.character,
            course=course,
            defaults={'hp': 100}
        )
        hp = course_character.hp
    else:
        hp = None
        progress = None
        total_points = None
        earned_points = None
    return render(request, 'courses/course_detail.html',
                  {'course': course, 'total_points': total_points, 'earned_points': earned_points, 'progress': progress,
                   'hp': hp})


@role_required('teacher')
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('courses:courses_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})
