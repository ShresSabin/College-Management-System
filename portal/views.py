import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q, Avg
from django.http import HttpResponseForbidden

from accounts.models import User, StudentProfile, TeacherProfile
from accounts.forms import StudentCreationForm, TeacherCreationForm
from .models import (
    Department, Course, Subject, TimetableSlot,
    AttendanceRecord, Assignment, AssignmentSubmission,
    Exam, Grade, Notice, LeaveRequest
)
from .forms import (
    NoticeForm, LeaveRequestForm, LeaveReviewForm,
    AssignmentForm, AssignmentSubmissionForm, GradeSubmissionForm,
    DepartmentForm, CourseForm, SubjectForm, TimetableSlotForm, ExamForm
)

def role_required(*allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in allowed_roles and not request.user.is_superuser:
                messages.error(request, "Access denied: You do not have permission to access this page.")
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# ==========================================
# ADMIN VIEWS
# ==========================================

@login_required
@role_required('ADMIN')
def admin_dashboard(request):
    total_students = StudentProfile.objects.count()
    total_teachers = TeacherProfile.objects.count()
    total_departments = Department.objects.count()
    total_courses = Course.objects.count()
    total_subjects = Subject.objects.count()
    pending_leaves = LeaveRequest.objects.filter(status='Pending').count()

    recent_students = StudentProfile.objects.select_related('user', 'department', 'course').order_by('-user__date_joined')[:5]
    recent_leaves = LeaveRequest.objects.select_related('user').order_by('-created_at')[:5]
    recent_notices = Notice.objects.select_related('posted_by').order_by('-created_at')[:4]

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_departments': total_departments,
        'total_courses': total_courses,
        'total_subjects': total_subjects,
        'pending_leaves': pending_leaves,
        'recent_students': recent_students,
        'recent_leaves': recent_leaves,
        'recent_notices': recent_notices,
    }
    return render(request, 'portal/admin/dashboard.html', context)


@login_required
@role_required('ADMIN')
def admin_students_list(request):
    query = request.GET.get('q', '')
    dept_id = request.GET.get('department')
    students = StudentProfile.objects.select_related('user', 'department', 'course').all()

    if query:
        students = students.filter(
            Q(roll_number__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__email__icontains=query)
        )
    if dept_id:
        students = students.filter(department_id=dept_id)

    departments = Department.objects.all()
    return render(request, 'portal/admin/students_list.html', {
        'students': students,
        'departments': departments,
        'query': query,
        'selected_dept': dept_id
    })


@login_required
@role_required('ADMIN')
def admin_student_create(request):
    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Student {student.get_full_name()} enrolled successfully!")
            return redirect('admin_students_list')
    else:
        form = StudentCreationForm()
    return render(request, 'portal/admin/student_form.html', {'form': form, 'title': 'Enroll New Student'})


@login_required
@role_required('ADMIN')
def admin_student_delete(request, pk):
    profile = get_object_or_404(StudentProfile, pk=pk)
    user = profile.user
    user.delete()
    messages.success(request, "Student removed successfully.")
    return redirect('admin_students_list')


@login_required
@role_required('ADMIN')
def admin_teachers_list(request):
    query = request.GET.get('q', '')
    teachers = TeacherProfile.objects.select_related('user', 'department').all()
    if query:
        teachers = teachers.filter(
            Q(employee_id__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(designation__icontains=query)
        )
    return render(request, 'portal/admin/teachers_list.html', {'teachers': teachers, 'query': query})


@login_required
@role_required('ADMIN')
def admin_teacher_create(request):
    if request.method == 'POST':
        form = TeacherCreationForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f"Faculty member {teacher.get_full_name()} added successfully!")
            return redirect('admin_teachers_list')
    else:
        form = TeacherCreationForm()
    return render(request, 'portal/admin/teacher_form.html', {'form': form, 'title': 'Add New Faculty Member'})


@login_required
@role_required('ADMIN')
def admin_teacher_delete(request, pk):
    profile = get_object_or_404(TeacherProfile, pk=pk)
    user = profile.user
    user.delete()
    messages.success(request, "Faculty member removed successfully.")
    return redirect('admin_teachers_list')


@login_required
@role_required('ADMIN')
def admin_departments(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department added successfully.")
            return redirect('admin_departments')
    else:
        form = DepartmentForm()
    departments = Department.objects.annotate(
        course_count=Count('courses'),
        teacher_count=Count('teachers')
    ).select_related('head_of_department')
    return render(request, 'portal/admin/departments.html', {'departments': departments, 'form': form})


@login_required
@role_required('ADMIN')
def admin_courses(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course created successfully.")
            return redirect('admin_courses')
    else:
        form = CourseForm()
    courses = Course.objects.annotate(
        subject_count=Count('subjects'),
        student_count=Count('students')
    ).select_related('department')
    return render(request, 'portal/admin/courses.html', {'courses': courses, 'form': form})


@login_required
@role_required('ADMIN')
def admin_subjects(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject created successfully.")
            return redirect('admin_subjects')
    else:
        form = SubjectForm()
    subjects = Subject.objects.select_related('course', 'teacher').all()
    return render(request, 'portal/admin/subjects.html', {'subjects': subjects, 'form': form})


@login_required
@role_required('ADMIN')
def admin_timetable(request):
    if request.method == 'POST':
        form = TimetableSlotForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Timetable slot added successfully.")
            return redirect('admin_timetable')
    else:
        form = TimetableSlotForm()
    slots = TimetableSlot.objects.select_related('subject', 'subject__course', 'subject__teacher').all()
    return render(request, 'portal/admin/timetable.html', {'slots': slots, 'form': form})


@login_required
@role_required('ADMIN')
def admin_leaves(request):
    leaves = LeaveRequest.objects.select_related('user', 'reviewed_by').all()
    status_filter = request.GET.get('status')
    if status_filter:
        leaves = leaves.filter(status=status_filter)
    return render(request, 'portal/admin/leaves.html', {'leaves': leaves, 'status_filter': status_filter})


@login_required
@role_required('ADMIN')
def admin_leave_review(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        note = request.POST.get('response_note', '')
        if action in ['Approved', 'Rejected']:
            leave.status = action
            leave.response_note = note
            leave.reviewed_by = request.user
            leave.save()
            messages.success(request, f"Leave request marked as {action}.")
    return redirect('admin_leaves')


@login_required
def notices_list(request):
    notices = Notice.objects.select_related('posted_by').all()
    if not (request.user.is_admin_user or request.user.is_superuser):
        notices = notices.filter(Q(target_role='ALL') | Q(target_role=request.user.role))
    
    if request.method == 'POST' and (request.user.is_admin_user or request.user.is_teacher_user):
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.posted_by = request.user
            notice.save()
            messages.success(request, "Notice published successfully.")
            return redirect('notices_list')
    else:
        form = NoticeForm()
    
    return render(request, 'portal/shared/notices.html', {'notices': notices, 'form': form})


# ==========================================
# TEACHER VIEWS
# ==========================================

@login_required
@role_required('TEACHER')
def teacher_dashboard(request):
    subjects = Subject.objects.filter(teacher=request.user).select_related('course')
    today_name = timezone.now().strftime('%A')
    today_schedule = TimetableSlot.objects.filter(
        subject__teacher=request.user,
        day_of_week=today_name
    ).select_related('subject')

    recent_assignments = Assignment.objects.filter(teacher=request.user).order_by('-created_at')[:4]
    pending_submissions = AssignmentSubmission.objects.filter(
        assignment__teacher=request.user,
        status='Submitted'
    ).count()

    my_leaves = LeaveRequest.objects.filter(user=request.user).order_by('-created_at')[:4]

    context = {
        'subjects': subjects,
        'today_schedule': today_schedule,
        'recent_assignments': recent_assignments,
        'pending_submissions': pending_submissions,
        'my_leaves': my_leaves,
        'today_name': today_name,
    }
    return render(request, 'portal/teacher/dashboard.html', context)


@login_required
@role_required('TEACHER')
def teacher_attendance_subject_list(request):
    subjects = Subject.objects.filter(teacher=request.user).select_related('course')
    return render(request, 'portal/teacher/attendance_subject_list.html', {'subjects': subjects})


@login_required
@role_required('TEACHER')
def teacher_take_attendance(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, teacher=request.user)
    date_str = request.GET.get('date', timezone.now().strftime('%Y-%m-%d'))
    try:
        attendance_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        attendance_date = timezone.now().date()

    # Get students belonging to subject's course and semester
    students = StudentProfile.objects.filter(
        course=subject.course,
        semester=subject.semester
    ).select_related('user').order_by('roll_number')

    if request.method == 'POST':
        for student_profile in students:
            status_val = request.POST.get(f'status_{student_profile.user.id}', 'Present')
            remarks_val = request.POST.get(f'remarks_{student_profile.user.id}', '')
            AttendanceRecord.objects.update_or_create(
                subject=subject,
                student=student_profile.user,
                date=attendance_date,
                defaults={
                    'status': status_val,
                    'remarks': remarks_val,
                    'recorded_by': request.user
                }
            )
        messages.success(request, f"Attendance for {subject.name} on {attendance_date} recorded successfully!")
        return redirect('teacher_attendance_history', subject_id=subject.id)

    # Fetch existing records for this date if already taken
    existing_records = {
        rec.student_id: rec
        for rec in AttendanceRecord.objects.filter(subject=subject, date=attendance_date)
    }

    student_data = []
    for s in students:
        rec = existing_records.get(s.user.id)
        student_data.append({
            'profile': s,
            'status': rec.status if rec else 'Present',
            'remarks': rec.remarks if rec else ''
        })

    context = {
        'subject': subject,
        'date_str': date_str,
        'attendance_date': attendance_date,
        'student_data': student_data,
    }
    return render(request, 'portal/teacher/take_attendance.html', context)


@login_required
@role_required('TEACHER')
def teacher_attendance_history(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, teacher=request.user)
    records = AttendanceRecord.objects.filter(subject=subject).select_related('student', 'student__student_profile').order_by('-date', 'student__student_profile__roll_number')
    
    # Calculate summary
    total_records = records.count()
    present_count = records.filter(status='Present').count()
    absent_count = records.filter(status='Absent').count()
    late_count = records.filter(status='Late').count()

    context = {
        'subject': subject,
        'records': records[:100],
        'total_records': total_records,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
    }
    return render(request, 'portal/teacher/attendance_history.html', context)


@login_required
@role_required('TEACHER')
def teacher_assignments(request):
    subjects = Subject.objects.filter(teacher=request.user)
    assignments = Assignment.objects.filter(teacher=request.user).annotate(
        submission_count=Count('submissions')
    ).select_related('subject')

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, teacher=request.user)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = request.user
            assignment.save()
            messages.success(request, f"Assignment '{assignment.title}' created successfully!")
            return redirect('teacher_assignments')
    else:
        form = AssignmentForm(teacher=request.user)

    return render(request, 'portal/teacher/assignments.html', {
        'assignments': assignments,
        'form': form,
        'subjects': subjects
    })


@login_required
@role_required('TEACHER')
def teacher_assignment_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, teacher=request.user)
    submissions = AssignmentSubmission.objects.filter(assignment=assignment).select_related('student', 'student__student_profile')
    return render(request, 'portal/teacher/submissions.html', {
        'assignment': assignment,
        'submissions': submissions
    })


@login_required
@role_required('TEACHER')
def teacher_grade_submission(request, submission_id):
    submission = get_object_or_404(AssignmentSubmission, id=submission_id, assignment__teacher=request.user)
    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, f"Graded submission for {submission.student.get_full_name()}.")
            return redirect('teacher_assignment_submissions', assignment_id=submission.assignment.id)
    else:
        form = GradeSubmissionForm(instance=submission)
    return render(request, 'portal/teacher/grade_submission.html', {
        'submission': submission,
        'form': form
    })


@login_required
@role_required('TEACHER')
def teacher_exams(request):
    subjects = Subject.objects.filter(teacher=request.user)
    exams = Exam.objects.filter(subject__teacher=request.user).select_related('subject')

    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save()
            messages.success(request, f"Exam '{exam.name}' created.")
            return redirect('teacher_exams')
    else:
        form = ExamForm()
        form.fields['subject'].queryset = subjects

    return render(request, 'portal/teacher/exams.html', {'exams': exams, 'form': form, 'subjects': subjects})


@login_required
@role_required('TEACHER')
def teacher_exam_grade_entry(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id, subject__teacher=request.user)
    students = StudentProfile.objects.filter(
        course=exam.subject.course,
        semester=exam.subject.semester
    ).select_related('user').order_by('roll_number')

    if request.method == 'POST':
        for s in students:
            marks_str = request.POST.get(f'marks_{s.user.id}')
            remarks = request.POST.get(f'remarks_{s.user.id}', '')
            if marks_str is not None and marks_str.strip() != '':
                try:
                    marks = float(marks_str)
                    grade_obj, _ = Grade.objects.get_or_create(exam=exam, student=s.user, defaults={'marks_obtained': marks})
                    grade_obj.marks_obtained = marks
                    grade_obj.remarks = remarks
                    grade_obj.letter_grade = grade_obj.calculate_letter_grade()
                    grade_obj.save()
                except ValueError:
                    pass
        messages.success(request, "Exam grades recorded and updated successfully!")
        return redirect('teacher_exams')

    existing_grades = {g.student_id: g for g in Grade.objects.filter(exam=exam)}
    student_grades = []
    for s in students:
        g = existing_grades.get(s.user.id)
        student_grades.append({
            'profile': s,
            'marks': g.marks_obtained if g else '',
            'grade': g.letter_grade if g else '',
            'remarks': g.remarks if g else ''
        })

    return render(request, 'portal/teacher/grade_entry.html', {'exam': exam, 'student_grades': student_grades})


@login_required
@role_required('TEACHER', 'STUDENT')
def user_leave_requests(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            messages.success(request, "Leave application submitted successfully for administrative review.")
            return redirect('user_leave_requests')
    else:
        form = LeaveRequestForm()

    leaves = LeaveRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'portal/shared/leave_requests.html', {'leaves': leaves, 'form': form})


# ==========================================
# STUDENT VIEWS
# ==========================================

@login_required
@role_required('STUDENT')
def student_dashboard(request):
    try:
        profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile not found. Please contact administration.")
        return redirect('profile')

    enrolled_subjects = Subject.objects.filter(course=profile.course, semester=profile.semester).select_related('teacher')
    
    # Overall attendance calculations
    total_classes = AttendanceRecord.objects.filter(student=request.user).count()
    present_classes = AttendanceRecord.objects.filter(student=request.user, status='Present').count()
    late_classes = AttendanceRecord.objects.filter(student=request.user, status='Late').count()
    
    attendance_pct = 0
    if total_classes > 0:
        # Give full credit for present and 0.5 for late
        attendance_pct = round(((present_classes + (late_classes * 0.5)) / total_classes) * 100, 1)

    today_name = timezone.now().strftime('%A')
    today_schedule = TimetableSlot.objects.filter(
        subject__in=enrolled_subjects,
        day_of_week=today_name
    ).select_related('subject')

    # Pending & upcoming assignments
    assignments = Assignment.objects.filter(subject__in=enrolled_subjects).order_by('due_date')
    submissions = {s.assignment_id: s for s in AssignmentSubmission.objects.filter(student=request.user)}

    assignment_cards = []
    for a in assignments[:5]:
        sub = submissions.get(a.id)
        assignment_cards.append({
            'assignment': a,
            'submission': sub,
            'is_submitted': sub is not None,
            'status': sub.status if sub else 'Pending',
        })

    # Recent grades
    recent_grades = Grade.objects.filter(student=request.user).select_related('exam', 'exam__subject').order_by('-exam__exam_date')[:5]

    # Notices
    notices = Notice.objects.filter(Q(target_role='ALL') | Q(target_role='STUDENT')).order_by('-is_pinned', '-created_at')[:4]

    context = {
        'profile': profile,
        'enrolled_subjects': enrolled_subjects,
        'total_classes': total_classes,
        'present_classes': present_classes,
        'attendance_pct': attendance_pct,
        'today_schedule': today_schedule,
        'today_name': today_name,
        'assignment_cards': assignment_cards,
        'recent_grades': recent_grades,
        'notices': notices,
    }
    return render(request, 'portal/student/dashboard.html', context)


@login_required
@role_required('STUDENT')
def student_attendance_view(request):
    profile = request.user.student_profile
    subjects = Subject.objects.filter(course=profile.course, semester=profile.semester)
    
    subject_stats = []
    overall_total = 0
    overall_attended = 0

    for sub in subjects:
        total = AttendanceRecord.objects.filter(student=request.user, subject=sub).count()
        present = AttendanceRecord.objects.filter(student=request.user, subject=sub, status='Present').count()
        late = AttendanceRecord.objects.filter(student=request.user, subject=sub, status='Late').count()
        absent = AttendanceRecord.objects.filter(student=request.user, subject=sub, status='Absent').count()
        
        pct = round(((present + (late * 0.5)) / total * 100), 1) if total > 0 else 0
        overall_total += total
        overall_attended += present + (late * 0.5)

        subject_stats.append({
            'subject': sub,
            'total': total,
            'present': present,
            'late': late,
            'absent': absent,
            'percentage': pct,
        })

    overall_pct = round((overall_attended / overall_total * 100), 1) if overall_total > 0 else 0
    recent_logs = AttendanceRecord.objects.filter(student=request.user).select_related('subject').order_by('-date')[:30]

    return render(request, 'portal/student/attendance.html', {
        'subject_stats': subject_stats,
        'overall_pct': overall_pct,
        'overall_total': overall_total,
        'overall_attended': overall_attended,
        'recent_logs': recent_logs
    })


@login_required
@role_required('STUDENT')
def student_timetable_view(request):
    profile = request.user.student_profile
    subjects = Subject.objects.filter(course=profile.course, semester=profile.semester)
    slots = TimetableSlot.objects.filter(subject__in=subjects).select_related('subject', 'subject__teacher').order_by('day_of_week', 'start_time')
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    timetable_by_day = {day: [] for day in days}
    for slot in slots:
        if slot.day_of_week in timetable_by_day:
            timetable_by_day[slot.day_of_week].append(slot)

    return render(request, 'portal/student/timetable.html', {
        'timetable_by_day': timetable_by_day,
        'profile': profile
    })


@login_required
@role_required('STUDENT')
def student_assignments_view(request):
    profile = request.user.student_profile
    subjects = Subject.objects.filter(course=profile.course, semester=profile.semester)
    assignments = Assignment.objects.filter(subject__in=subjects).select_related('subject', 'teacher').order_by('due_date')
    
    submissions = {s.assignment_id: s for s in AssignmentSubmission.objects.filter(student=request.user)}
    
    assignment_items = []
    for a in assignments:
        sub = submissions.get(a.id)
        assignment_items.append({
            'assignment': a,
            'submission': sub,
            'is_submitted': sub is not None,
            'is_past_due': a.due_date < timezone.now()
        })

    return render(request, 'portal/student/assignments.html', {'assignments': assignment_items})


@login_required
@role_required('STUDENT')
def student_submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submission = AssignmentSubmission.objects.filter(assignment=assignment, student=request.user).first()

    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.assignment = assignment
            sub.student = request.user
            if assignment.due_date < timezone.now():
                sub.status = 'Late'
            else:
                sub.status = 'Submitted'
            sub.save()
            messages.success(request, f"Your assignment '{assignment.title}' was submitted successfully!")
            return redirect('student_assignments_view')
    else:
        form = AssignmentSubmissionForm(instance=submission)

    return render(request, 'portal/student/submit_assignment.html', {
        'assignment': assignment,
        'submission': submission,
        'form': form
    })


@login_required
@role_required('STUDENT')
def student_results_view(request):
    grades = Grade.objects.filter(student=request.user).select_related('exam', 'exam__subject').order_by('-exam__exam_date')
    
    total_marks_obtained = sum(float(g.marks_obtained) for g in grades)
    total_max_marks = sum(g.exam.max_marks for g in grades)
    overall_percentage = round((total_marks_obtained / total_max_marks * 100), 1) if total_max_marks > 0 else 0

    return render(request, 'portal/student/results.html', {
        'grades': grades,
        'overall_percentage': overall_percentage,
        'total_exams': grades.count()
    })
