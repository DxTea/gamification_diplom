import os
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import Http404, FileResponse, HttpResponseRedirect
from django.urls import reverse

from courses.models import Course
from .models import Assignment, SubmittedAssignment
from .forms import AssignmentForm, \
    SubmittedAssignmentForm

from django.contrib.auth.decorators import login_required

from users.decorators import role_required


@role_required('teacher')
def assignment_create(request, pk):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course_id = pk
            if assignment.assignment_type != 'theory' and not assignment.weight:
                num_assignments = Assignment.objects.filter(course_id=pk).exclude(assignment_type='theory').count()
                assignment.weight = 1 / (num_assignments + 1)
            assignment.save()
            return redirect('courses:course_detail', pk=pk)
    else:
        form = AssignmentForm()
    return render(request, 'assignments/assignment_create.html', {'form': form})


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if assignment.assignment_type == 'theory':
        if request.method == 'POST':
            submitted_assignment, created = SubmittedAssignment.objects.get_or_create(
                assignment=assignment,
                student=request.user,
                defaults={'grade': 100, 'reviewed': True}
            )
            if created:
                return redirect('assignments:assignment_detail', pk=pk)
        else:
            try:
                submitted_assignment = SubmittedAssignment.objects.get(assignment=assignment, student=request.user)
            except SubmittedAssignment.DoesNotExist:
                submitted_assignment = None

            context = {
                'assignment': assignment,
                'TIME_ZONE': timezone.get_current_timezone_name(),
                'submitted_assignment': submitted_assignment,
            }
            return render(request, 'assignments/assignment_detail.html', context)
    else:
        if request.method == 'POST':
            submitted_assignment, created = SubmittedAssignment.objects.get_or_create(
                assignment=assignment,
                student=request.user,
                defaults={'file': None}
            )
            form = SubmittedAssignmentForm(request.POST, request.FILES, instance=submitted_assignment)
            if form.is_valid():
                submitted_assignment = form.save(commit=False)
                submitted_assignment.student = request.user
                submitted_assignment.assignment = assignment
                submitted_assignment.save()
                return redirect('assignments:assignment_detail', pk=pk)
        else:
            try:
                submitted_assignment = SubmittedAssignment.objects.get(assignment=assignment, student=request.user)
                form = SubmittedAssignmentForm(instance=submitted_assignment)
            except SubmittedAssignment.DoesNotExist:
                form = SubmittedAssignmentForm()
        context = {
            'assignment': assignment,
            'form': form,
            'submitted_assignment': submitted_assignment if 'submitted_assignment' in locals() else None,
            'TIME_ZONE': timezone.get_current_timezone_name(),
        }
        return render(request, 'assignments/assignment_detail.html', context)


@role_required('teacher')
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        course_id = assignment.course_id
        assignment.delete()
        return redirect('courses:course_detail', pk=course_id)
    return render(request, 'assignments/assignment_confirm_delete.html', {'assignment': assignment})


@role_required('teacher')
def assignment_edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.save()
            form.save_m2m()
            return redirect('assignments:assignment_detail', pk=assignment.pk)
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'assignments/assignment_edit.html', {'form': form})


@role_required('teacher')
def review_assignments(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    reviewed_assignments = SubmittedAssignment.objects.filter(reviewed=True)
    unreviewed_assignments = SubmittedAssignment.objects.filter(reviewed=False)
    context = {
        'course': course,
        'reviewed_assignments': reviewed_assignments,
        'unreviewed_assignments': unreviewed_assignments,
    }
    return render(request, 'assignments/review_assignments.html', context)


@role_required('teacher')
def grade_assignment(request, pk):
    if request.method == 'POST':
        assignment = get_object_or_404(SubmittedAssignment, pk=pk)
        grade = request.POST.get('grade')
        if grade:
            assignment.grade = int(grade)
            assignment.reviewed = True
            assignment.calculate_experience()
            assignment.calculate_damage()
            assignment.save()
            assignment.student.character.experience += assignment.experience_gained
            assignment.student.character.update_level()
            assignment.student.character.save()
        return HttpResponseRedirect(reverse('assignments:review_assignments', args=[assignment.assignment.course.id]))


@login_required
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        raise Http404
