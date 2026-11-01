from django import forms
from .models import (
    Department, Course, Subject, TimetableSlot,
    AttendanceRecord, Assignment, AssignmentSubmission,
    Exam, Grade, Notice, LeaveRequest
)
from accounts.models import User

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'target_role', 'is_pinned']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notice Headline'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter announcement details...'}),
            'target_role': forms.Select(attrs={'class': 'form-select'}),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'State the reason for your leave request...'}),
        }


class LeaveReviewForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['status', 'response_note']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'response_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional remarks/feedback'}),
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['subject', 'title', 'description', 'due_date', 'max_marks', 'attachment']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Assignment title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Instructions and details'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['subject'].queryset = Subject.objects.filter(teacher=teacher)


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['submission_text', 'submission_file']
        widgets = {
            'submission_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Type your submission response, notes, or links...'}),
            'submission_file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['marks_obtained', 'feedback', 'status']
        widgets = {
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Feedback for the student'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'head_of_department']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'head_of_department': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['head_of_department'].queryset = User.objects.filter(role='TEACHER')


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'department', 'total_semesters', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'total_semesters': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'course', 'semester', 'credits', 'teacher']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = User.objects.filter(role='TEACHER')


class TimetableSlotForm(forms.ModelForm):
    class Meta:
        model = TimetableSlot
        fields = ['subject', 'day_of_week', 'start_time', 'end_time', 'room_number']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'day_of_week': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'subject', 'exam_date', 'max_marks', 'pass_marks']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Midterm Spring 2026'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'pass_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }
