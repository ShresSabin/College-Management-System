from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Department(models.Model):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=15, unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Course(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    total_semesters = models.PositiveSmallIntegerField(default=8)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Subject(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    semester = models.PositiveSmallIntegerField(default=1)
    credits = models.PositiveSmallIntegerField(default=3)
    teacher = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='taught_subjects'
    )

    def __str__(self):
        return f"{self.code} - {self.name}"


class TimetableSlot(models.Model):
    DAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetable_slots')
    day_of_week = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=30, default='Room 101')

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.day_of_week} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}): {self.subject.name} [{self.room_number}]"


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')
    remarks = models.CharField(max_length=150, blank=True)
    recorded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recorded_attendances'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subject', 'student', 'date')
        ordering = ['-date', 'student']

    def __str__(self):
        return f"{self.student.username} - {self.subject.code} - {self.date}: {self.status}"


class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_marks = models.PositiveIntegerField(default=100)
    attachment = models.FileField(upload_to='assignments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-due_date']

    def __str__(self):
        return f"{self.title} ({self.subject.code})"


class AssignmentSubmission(models.Model):
    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Graded', 'Graded'),
        ('Late', 'Late'),
    ]
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignment_submissions')
    submission_file = models.FileField(upload_to='submissions/', blank=True, null=True)
    submission_text = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Submitted')

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"


class Exam(models.Model):
    name = models.CharField(max_length=150)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    exam_date = models.DateField()
    max_marks = models.PositiveIntegerField(default=100)
    pass_marks = models.PositiveIntegerField(default=40)

    def __str__(self):
        return f"{self.name} - {self.subject.code}"


class Grade(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    letter_grade = models.CharField(max_length=5, blank=True)
    remarks = models.CharField(max_length=150, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('exam', 'student')

    def calculate_letter_grade(self):
        percentage = (float(self.marks_obtained) / self.exam.max_marks) * 100
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B+'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'

    def save(self, *args, **kwargs):
        if not self.letter_grade:
            self.letter_grade = self.calculate_letter_grade()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.exam.name}: {self.marks_obtained}/{self.exam.max_marks} ({self.letter_grade})"


class Notice(models.Model):
    TARGET_ROLES = [
        ('ALL', 'All Users'),
        ('STUDENT', 'Students Only'),
        ('TEACHER', 'Teachers Only'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notices')
    target_role = models.CharField(max_length=10, choices=TARGET_ROLES, default='ALL')
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title


class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    response_note = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_leaves'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.status} ({self.start_date} to {self.end_date})"
