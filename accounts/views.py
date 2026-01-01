from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages




def student_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('student_register')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        Profile.objects.create(user=user, is_student=True)

        

        messages.success(request, 'Registration successful. Please login.')
        return redirect('student_login')

    return render(request, 'accounts/student_register.html')



from django.contrib.auth.models import User

def student_login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )
            except User.DoesNotExist:
                user = None

        if user is not None:
            profile = Profile.objects.get(user=user)
            if profile.is_student:
                login(request, user)
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Not a student account')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/student_login.html')





def logout_view(request):
    logout(request)
    return redirect('student_login')