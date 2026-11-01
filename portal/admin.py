from django.contrib import admin
from .models import (
    Department, Course, Subject, TimetableSlot,
    AttendanceRecord, Assignment, AssignmentSubmission,
    Exam, Grade, Notice, LeaveRequest
)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head_of_department', 'created_at')
    search_fields = ('name', 'code')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'total_semesters')
    list_filter = ('department',)
    search_fields = ('name', 'code')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'course', 'semester', 'credits', 'teacher')
    list_filter = ('course__department', 'course', 'semester')
    search_fields = ('code', 'name')

@admin.register(TimetableSlot)
class TimetableSlotAdmin(admin.ModelAdmin):
    list_display = ('subject', 'day_of_week', 'start_time', 'end_time', 'room_number')
    list_filter = ('day_of_week', 'subject__course')

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'subject', 'student', 'status', 'recorded_by')
    list_filter = ('status', 'date', 'subject')
    search_fields = ('student__username', 'student__first_name', 'student__last_name', 'subject__name')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'due_date', 'max_marks')
    list_filter = ('subject', 'due_date')
    search_fields = ('title', 'description')

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'status', 'submitted_at', 'marks_obtained')
    list_filter = ('status', 'assignment__subject')
    search_fields = ('student__username', 'assignment__title')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'exam_date', 'max_marks', 'pass_marks')
    list_filter = ('subject', 'exam_date')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'marks_obtained', 'letter_grade')
    list_filter = ('exam__subject', 'letter_grade')
    search_fields = ('student__username', 'exam__name')

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_role', 'posted_by', 'is_pinned', 'created_at')
    list_filter = ('target_role', 'is_pinned', 'created_at')
    search_fields = ('title', 'content')

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'status', 'created_at', 'reviewed_by')
    list_filter = ('status', 'user__role')
    search_fields = ('user__username', 'reason')
