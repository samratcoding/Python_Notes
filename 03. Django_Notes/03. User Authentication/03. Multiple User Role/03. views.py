from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import AppUser, Task, TaskPermission
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import AppUser, Teacher, Student

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # Handle invalid login

    return render(request, 'login.html')

def dashboard(request):
    if request.user.is_teacher:
        # Display teacher dashboard
        tasks = Task.objects.filter(assigned_to=request.user)
    elif request.user.is_student:
        # Display student dashboard
        tasks = Task.objects.filter(assigned_to=request.user)
    else:
        # Handle other user types
        tasks = []

    return render(request, 'dashboard.html', {'tasks': tasks})



@login_required
def remove_student(request, student_id):
    # Check if the user is a teacher
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if not user_profile.teachers.exists():
        return redirect('profile')  # Redirect to the profile page if not a teacher

    student = get_object_or_404(UserProfile, id=student_id)

    # Check if the student is one of the teacher's students
    if student in user_profile.students.all():
        # Remove the student from the teacher's list of students
        user_profile.students.remove(student)
        return redirect('profile')  # Redirect to the profile page
    else:
        return redirect('profile')  # Redirect to the profile page if the student is not a student of the teacher

