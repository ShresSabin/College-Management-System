from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, TeacherProfile

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile'
    fk_name = 'user'

class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    can_delete = False
    verbose_name_plural = 'Teacher Profile'
    fk_name = 'user'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Additional Info', {
            'fields': ('role', 'phone', 'gender', 'date_of_birth', 'address', 'profile_pic')
        }),
    )
    inlines = [StudentProfileInline, TeacherProfileInline]

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'user', 'department', 'course', 'semester', 'batch_year')
    search_fields = ('roll_number', 'user__username', 'user__first_name', 'user__last_name')
    list_filter = ('department', 'course', 'semester', 'batch_year')

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'department', 'designation', 'joining_date')
    search_fields = ('employee_id', 'user__username', 'user__first_name', 'user__last_name')
    list_filter = ('department', 'designation')
