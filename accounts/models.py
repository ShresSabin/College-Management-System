from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    phone = models.CharField(max_length=20, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    @property
    def is_admin_user(self):
        return self.role == 'ADMIN' or self.is_superuser

    @property
    def is_teacher_user(self):
        return self.role == 'TEACHER'

    @property
    def is_student_user(self):
        return self.role == 'STUDENT'

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.username


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=30, unique=True)
    department = models.ForeignKey('portal.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    course = models.ForeignKey('portal.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    semester = models.PositiveSmallIntegerField(default=1)
    batch_year = models.PositiveIntegerField(default=2024)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=30, unique=True)
    department = models.ForeignKey('portal.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
    designation = models.CharField(max_length=100, default='Lecturer')
    qualification = models.CharField(max_length=150, blank=True)
    joining_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.designation} {self.user.get_full_name()} ({self.employee_id})"
