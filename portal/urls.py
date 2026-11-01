from django.urls import path
from . import views

urlpatterns = [
    # Admin URLs
    path('admin-portal/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-portal/students/', views.admin_students_list, name='admin_students_list'),
    path('admin-portal/students/add/', views.admin_student_create, name='admin_student_create'),
    path('admin-portal/students/<int:pk>/delete/', views.admin_student_delete, name='admin_student_delete'),
    path('admin-portal/teachers/', views.admin_teachers_list, name='admin_teachers_list'),
    path('admin-portal/teachers/add/', views.admin_teacher_create, name='admin_teacher_create'),
    path('admin-portal/teachers/<int:pk>/delete/', views.admin_teacher_delete, name='admin_teacher_delete'),
    path('admin-portal/departments/', views.admin_departments, name='admin_departments'),
    path('admin-portal/courses/', views.admin_courses, name='admin_courses'),
    path('admin-portal/subjects/', views.admin_subjects, name='admin_subjects'),
    path('admin-portal/timetable/', views.admin_timetable, name='admin_timetable'),
    path('admin-portal/leaves/', views.admin_leaves, name='admin_leaves'),
    path('admin-portal/leaves/<int:pk>/review/', views.admin_leave_review, name='admin_leave_review'),

    # Shared URLs
    path('notices/', views.notices_list, name='notices_list'),
    path('leave-requests/', views.user_leave_requests, name='user_leave_requests'),

    # Teacher URLs
    path('teacher-portal/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher-portal/attendance/', views.teacher_attendance_subject_list, name='teacher_attendance_subjects'),
    path('teacher-portal/attendance/<int:subject_id>/take/', views.teacher_take_attendance, name='teacher_take_attendance'),
    path('teacher-portal/attendance/<int:subject_id>/history/', views.teacher_attendance_history, name='teacher_attendance_history'),
    path('teacher-portal/assignments/', views.teacher_assignments, name='teacher_assignments'),
    path('teacher-portal/assignments/<int:assignment_id>/submissions/', views.teacher_assignment_submissions, name='teacher_assignment_submissions'),
    path('teacher-portal/submissions/<int:submission_id>/grade/', views.teacher_grade_submission, name='teacher_grade_submission'),
    path('teacher-portal/exams/', views.teacher_exams, name='teacher_exams'),
    path('teacher-portal/exams/<int:exam_id>/grades/', views.teacher_exam_grade_entry, name='teacher_exam_grades'),

    # Student URLs
    path('student-portal/', views.student_dashboard, name='student_dashboard'),
    path('student-portal/attendance/', views.student_attendance_view, name='student_attendance'),
    path('student-portal/timetable/', views.student_timetable_view, name='student_timetable'),
    path('student-portal/assignments/', views.student_assignments_view, name='student_assignments_view'),
    path('student-portal/assignments/<int:assignment_id>/submit/', views.student_submit_assignment, name='student_submit_assignment'),
    path('student-portal/results/', views.student_results_view, name='student_results'),
]
