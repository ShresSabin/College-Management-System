from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserProfileForm
from .models import User

LOGIN_ROLES = {
    'ADMIN': 'Administrator',
    'TEACHER': 'Professor',
    'STUDENT': 'Student',
}


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    selected_role = request.POST.get('role') if request.method == 'POST' else request.GET.get('role')
    if selected_role not in LOGIN_ROLES:
        selected_role = None

    if request.method == 'POST':
        if selected_role is None:
            messages.error(request, "Choose an account type before signing in.")
            return redirect('login')

        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                user_role = 'ADMIN' if user.is_admin_user else user.role
                if user_role == selected_role:
                    login(request, user)
                    messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                    return redirect('dashboard')
                messages.error(
                    request,
                    f"This account is not registered as a {LOGIN_ROLES[selected_role].lower()}. "
                    "Choose the correct account type and try again."
                )
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form,
        'selected_role': selected_role,
        'selected_role_label': LOGIN_ROLES.get(selected_role),
        'login_roles': LOGIN_ROLES.items(),
    })


def custom_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


@login_required
def dashboard_redirect(request):
    if request.user.is_admin_user:
        return redirect('admin_dashboard')
    elif request.user.is_teacher_user:
        return redirect('teacher_dashboard')
    elif request.user.is_student_user:
        return redirect('student_dashboard')
    return redirect('login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile details have been updated successfully.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'user_obj': request.user
    })
