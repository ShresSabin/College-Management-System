import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User, StudentProfile, TeacherProfile
from portal.models import (
    Department, Course, Subject, TimetableSlot,
    AttendanceRecord, Assignment, AssignmentSubmission,
    Exam, Grade, Notice, LeaveRequest
)

class Command(BaseCommand):
    help = 'Seeds sample data for testing the College Management System'

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding...")

        # 1. Create Superuser / Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Rajesh',
                'last_name': 'Shrestha',
                'email': 'admin@projectcollege.edu.np',
                'role': 'ADMIN',
                'is_staff': True,
                'is_superuser': True,
                'phone': '+977-9841-000001',
                'gender': 'Male',
                'address': 'Ratnapark, Kathmandu, Bagmati Province'
            }
        )
        if created or not admin_user.check_password('admin123'):
            admin_user.set_password('admin123')
        admin_user.first_name = 'Rajesh'
        admin_user.last_name = 'Shrestha'
        admin_user.save()
        self.stdout.write(self.style.SUCCESS("Admin account ready: admin / admin123"))

        # 2. Departments
        dept_cse, _ = Department.objects.get_or_create(
            code='CSE',
            defaults={
                'name': 'Computer Science & Engineering',
                'description': 'Software nirman, artificial intelligence ra computing pranali ko adhyayan garne vibhag.'
            }
        )
        dept_it, _ = Department.objects.get_or_create(
            code='IT',
            defaults={
                'name': 'Information Technology',
                'description': 'Network sangrachana, cloud computing ra cybersecurity ma kendrit vibhag.'
            }
        )
        dept_mech, _ = Department.objects.get_or_create(
            code='MECH',
            defaults={
                'name': 'Mechanical Engineering',
                'description': 'Thermodynamics, robotics ra advanced nirman pranali ko adhyayan.'
            }
        )

        # 3. Courses
        course_btech_cs, _ = Course.objects.get_or_create(
            code='BTECH-CS',
            defaults={
                'name': 'B.Tech Computer Science',
                'department': dept_cse,
                'total_semesters': 8,
                'description': 'Char barsha ko degree jama algorithm, system ra software engineering samavesh cha.'
            }
        )
        course_btech_it, _ = Course.objects.get_or_create(
            code='BTECH-IT',
            defaults={
                'name': 'B.Tech Information Technology',
                'department': dept_it,
                'total_semesters': 8,
                'description': 'IT parikathna, suraksha ra web applications ma kendrit char barsha ko degree.'
            }
        )

        # 4. Teachers - Nepali names in English alphabets
        teachers_data = [
            {
                'username': 'dr_bikash',
                'first_name': 'Bikash',
                'last_name': 'Thapa',
                'email': 'bikash.thapa@projectcollege.edu.np',
                'role': 'TEACHER',
                'emp_id': 'EMP-CSE-101',
                'dept': dept_cse,
                'designation': 'Professor & Head',
                'qualification': 'Ph.D. Computer Science (Tribhuvan Vishwavidyalaya)',
                'phone': '+977-9841-112233',
            },
            {
                'username': 'prof_sunita',
                'first_name': 'Sunita',
                'last_name': 'Gurung',
                'email': 'sunita.gurung@projectcollege.edu.np',
                'role': 'TEACHER',
                'emp_id': 'EMP-CSE-102',
                'dept': dept_cse,
                'designation': 'Associate Professor',
                'qualification': 'M.Tech Software Engineering (Pokhara Vishwavidyalaya)',
                'phone': '+977-9852-223344',
            },
            {
                'username': 'dr_pradip',
                'first_name': 'Pradip',
                'last_name': 'Adhikari',
                'email': 'pradip.adhikari@projectcollege.edu.np',
                'role': 'TEACHER',
                'emp_id': 'EMP-IT-103',
                'dept': dept_it,
                'designation': 'Assistant Professor',
                'qualification': 'Ph.D. Information Systems (Kathmandu University)',
                'phone': '+977-9861-334455',
            }
        ]

        teacher_objs = {}
        for t_info in teachers_data:
            t_user, created = User.objects.get_or_create(
                username=t_info['username'],
                defaults={
                    'first_name': t_info['first_name'],
                    'last_name': t_info['last_name'],
                    'email': t_info['email'],
                    'role': t_info['role'],
                    'is_staff': True,
                    'phone': t_info['phone'],
                }
            )
            t_user.first_name = t_info['first_name']
            t_user.last_name = t_info['last_name']
            t_user.set_password('teacher123')
            t_user.save()
            TeacherProfile.objects.update_or_create(
                user=t_user,
                defaults={
                    'employee_id': t_info['emp_id'],
                    'department': t_info['dept'],
                    'designation': t_info['designation'],
                    'qualification': t_info['qualification'],
                    'joining_date': datetime.date(2021, 8, 15)
                }
            )
            teacher_objs[t_info['username']] = t_user

        dept_cse.head_of_department = teacher_objs['dr_bikash']
        dept_cse.save()

        # 5. Subjects
        sub_dsa, _ = Subject.objects.get_or_create(
            code='CS401',
            defaults={
                'name': 'Data Structures & Algorithms',
                'course': course_btech_cs,
                'semester': 4,
                'credits': 4,
                'teacher': teacher_objs['dr_bikash']
            }
        )
        sub_dbms, _ = Subject.objects.get_or_create(
            code='CS402',
            defaults={
                'name': 'Database Management Systems',
                'course': course_btech_cs,
                'semester': 4,
                'credits': 4,
                'teacher': teacher_objs['prof_sunita']
            }
        )
        sub_os, _ = Subject.objects.get_or_create(
            code='CS403',
            defaults={
                'name': 'Operating Systems & Concurrency',
                'course': course_btech_cs,
                'semester': 4,
                'credits': 3,
                'teacher': teacher_objs['dr_bikash']
            }
        )
        sub_web, _ = Subject.objects.get_or_create(
            code='IT401',
            defaults={
                'name': 'Full-Stack Web Technologies',
                'course': course_btech_it,
                'semester': 4,
                'credits': 4,
                'teacher': teacher_objs['dr_pradip']
            }
        )

        # 6. Students - Nepali names in English alphabets
        students_data = [
            {
                'username': 'student_aarav',
                'first_name': 'Aarav',
                'last_name': 'Sharma',
                'email': 'aarav.sharma@student.projectcollege.edu.np',
                'roll': 'CSE-2024-001',
                'course': course_btech_cs,
                'dept': dept_cse,
                'sem': 4,
                'guardian': 'Ramesh Sharma',
                'g_phone': '+977-9841-556677',
            },
            {
                'username': 'student_sita',
                'first_name': 'Sita',
                'last_name': 'Poudel',
                'email': 'sita.poudel@student.projectcollege.edu.np',
                'roll': 'CSE-2024-002',
                'course': course_btech_cs,
                'dept': dept_cse,
                'sem': 4,
                'guardian': 'Hari Poudel',
                'g_phone': '+977-9852-667788',
            },
            {
                'username': 'student_rohan',
                'first_name': 'Rohan',
                'last_name': 'Basnet',
                'email': 'rohan.basnet@student.projectcollege.edu.np',
                'roll': 'CSE-2024-003',
                'course': course_btech_cs,
                'dept': dept_cse,
                'sem': 4,
                'guardian': 'Binod Basnet',
                'g_phone': '+977-9861-778899',
            },
            {
                'username': 'student_maya',
                'first_name': 'Maya',
                'last_name': 'Tamang',
                'email': 'maya.tamang@student.projectcollege.edu.np',
                'roll': 'IT-2024-001',
                'course': course_btech_it,
                'dept': dept_it,
                'sem': 4,
                'guardian': 'Dawa Tamang',
                'g_phone': '+977-9841-889900',
            }
        ]

        student_objs = {}
        for s_info in students_data:
            s_user, created = User.objects.get_or_create(
                username=s_info['username'],
                defaults={
                    'first_name': s_info['first_name'],
                    'last_name': s_info['last_name'],
                    'email': s_info['email'],
                    'role': 'STUDENT',
                    'phone': '+977-9841-000000',
                }
            )
            s_user.first_name = s_info['first_name']
            s_user.last_name = s_info['last_name']
            s_user.set_password('student123')
            s_user.save()
            StudentProfile.objects.update_or_create(
                user=s_user,
                defaults={
                    'roll_number': s_info['roll'],
                    'department': s_info['dept'],
                    'course': s_info['course'],
                    'semester': s_info['sem'],
                    'batch_year': 2024,
                    'guardian_name': s_info['guardian'],
                    'guardian_phone': s_info['g_phone'],
                }
            )
            student_objs[s_info['username']] = s_user

        # 7. Timetable Slots
        slots = [
            (sub_dsa, 'Monday', '09:00:00', '10:30:00', 'Hall 301'),
            (sub_dbms, 'Monday', '11:00:00', '12:30:00', 'Lab 2'),
            (sub_os, 'Tuesday', '09:00:00', '10:30:00', 'Hall 302'),
            (sub_dsa, 'Wednesday', '10:00:00', '11:30:00', 'Hall 301'),
            (sub_dbms, 'Thursday', '14:00:00', '15:30:00', 'Lab 2'),
            (sub_web, 'Friday', '10:00:00', '11:30:00', 'Web Studio 4')
        ]
        for sub, day, st, et, room in slots:
            TimetableSlot.objects.get_or_create(
                subject=sub,
                day_of_week=day,
                start_time=st,
                end_time=et,
                defaults={'room_number': room}
            )

        # 8. Attendance Records
        today = timezone.now().date()
        for i in range(1, 11):
            past_date = today - datetime.timedelta(days=i)
            if past_date.weekday() < 5:
                AttendanceRecord.objects.get_or_create(
                    subject=sub_dsa,
                    student=student_objs['student_aarav'],
                    date=past_date,
                    defaults={
                        'status': 'Present' if i != 3 else 'Late',
                        'recorded_by': teacher_objs['dr_bikash']
                    }
                )
                AttendanceRecord.objects.get_or_create(
                    subject=sub_dbms,
                    student=student_objs['student_aarav'],
                    date=past_date,
                    defaults={
                        'status': 'Present' if i != 7 else 'Absent',
                        'recorded_by': teacher_objs['prof_sunita']
                    }
                )
                AttendanceRecord.objects.get_or_create(
                    subject=sub_dsa,
                    student=student_objs['student_sita'],
                    date=past_date,
                    defaults={
                        'status': 'Present',
                        'recorded_by': teacher_objs['dr_bikash']
                    }
                )
                AttendanceRecord.objects.get_or_create(
                    subject=sub_dsa,
                    student=student_objs['student_rohan'],
                    date=past_date,
                    defaults={
                        'status': 'Absent' if i in [2, 5] else 'Present',
                        'recorded_by': teacher_objs['dr_bikash']
                    }
                )

        # 9. Assignments & Submissions
        assign1, _ = Assignment.objects.get_or_create(
            subject=sub_dsa,
            title='AVL Tree ra Graph BFS/DFS ko Implement',
            teacher=teacher_objs['dr_bikash'],
            defaults={
                'description': 'C++ athawa Python ma AVL Tree (self-balancing) ra directed weighted graph ma BFS/DFS traversal implement garnus. Unit tests ra complexity analysis samavesh garnus.',
                'due_date': timezone.now() + datetime.timedelta(days=5),
                'max_marks': 50
            }
        )

        assign2, _ = Assignment.objects.get_or_create(
            subject=sub_dbms,
            title='Relational Schema Normalization ra SQL Queries',
            teacher=teacher_objs['prof_sunita'],
            defaults={
                'description': 'Hospital management ko lagi 3NF/BCNF normalized database schema design garnus. Complex aggregate reports, nested subqueries ra window functions ko SQL queries lekhnus.',
                'due_date': timezone.now() + datetime.timedelta(days=8),
                'max_marks': 100
            }
        )

        # Submissions for Aarav
        AssignmentSubmission.objects.get_or_create(
            assignment=assign1,
            student=student_objs['student_aarav'],
            defaults={
                'submission_text': 'AVL self-balancing rotations (LL, RR, LR, RL) O(log N) time complexity sita implement gareko. 10,000 synthetic nodes ma test gareko.',
                'marks_obtained': 47.50,
                'status': 'Graded',
                'feedback': 'Code structure ati ramro cha ra unit tests pani thorough cha. Badhai!'
            }
        )

        # Submissions for Sita
        AssignmentSubmission.objects.get_or_create(
            assignment=assign1,
            student=student_objs['student_sita'],
            defaults={
                'submission_text': 'AVL Tree graphical visualizer sita implement gareko, BFS pathfinder pani samavesh cha.',
                'marks_obtained': 49.00,
                'status': 'Graded',
                'feedback': 'Ati ramro submission! Visualizer ek dam sundar cha.'
            }
        )

        # 10. Exams & Grades
        midterm_dsa, _ = Exam.objects.get_or_create(
            name='Madhyakalin Pariksha 2081',
            subject=sub_dsa,
            defaults={
                'exam_date': today - datetime.timedelta(days=15),
                'max_marks': 100,
                'pass_marks': 40
            }
        )
        midterm_dbms, _ = Exam.objects.get_or_create(
            name='Madhyakalin Pariksha 2081',
            subject=sub_dbms,
            defaults={
                'exam_date': today - datetime.timedelta(days=12),
                'max_marks': 100,
                'pass_marks': 40
            }
        )

        Grade.objects.get_or_create(
            exam=midterm_dsa,
            student=student_objs['student_aarav'],
            defaults={'marks_obtained': 92.50, 'letter_grade': 'A+', 'remarks': 'Ati ramro prastuti'}
        )
        Grade.objects.get_or_create(
            exam=midterm_dbms,
            student=student_objs['student_aarav'],
            defaults={'marks_obtained': 86.00, 'letter_grade': 'A', 'remarks': 'Dharana ekdam spashta cha'}
        )
        Grade.objects.get_or_create(
            exam=midterm_dsa,
            student=student_objs['student_sita'],
            defaults={'marks_obtained': 95.00, 'letter_grade': 'A+', 'remarks': 'Kaksha ko topper'}
        )

        # 11. Notices
        Notice.objects.get_or_create(
            title='Barshik Prabidhi Mahotsav ra Hackathon 2081',
            posted_by=admin_user,
            defaults={
                'content': 'Aayami mahina hunne Project College Hackathon 2081 ko ghoshana garda khushi lagdacha. Darta Sombar dekhi suru. Jamma purashkar rashi NPR 1,00,000! 3-4 janako team le student portal bata darta garna sakcha.',
                'target_role': 'ALL',
                'is_pinned': True
            }
        )
        Notice.objects.get_or_create(
            title='Shikshakharuko Madhyakalin Anka Bujhaune Antim Darta',
            posted_by=admin_user,
            defaults={
                'content': 'Sabai vibhagka shikshakharulai Shukrabar beluka 5:00 bajebhitra madhyakalin pariksha ko anka bujaunu hunu ko anurodh garindacha.',
                'target_role': 'TEACHER',
                'is_pinned': False
            }
        )
        Notice.objects.get_or_create(
            title='Pariksha Kaalma Pustakalaya Badhawa Samay',
            posted_by=admin_user,
            defaults={
                'content': 'Kendriyo Digital Pustakalaya aayami Sombar dekhi 24/7 khula rahane cha. Adhyayan kaksha agraim buki garna sakcha.',
                'target_role': 'STUDENT',
                'is_pinned': False
            }
        )

        # 12. Leave Requests
        LeaveRequest.objects.get_or_create(
            user=student_objs['student_aarav'],
            start_date=today + datetime.timedelta(days=3),
            end_date=today + datetime.timedelta(days=4),
            defaults={
                'reason': 'Antarwishwavidyalaya Rashtriya Coding Olympiad ma college ko pratinidhi bhanera sahabhagi hunalai.',
                'status': 'Approved',
                'reviewed_by': admin_user,
                'response_note': 'Swikrit. Hamro sanstha ko pratinidhitwa garda shubhakamana!'
            }
        )
        LeaveRequest.objects.get_or_create(
            user=teacher_objs['prof_sunita'],
            start_date=today + datetime.timedelta(days=10),
            end_date=today + datetime.timedelta(days=11),
            defaults={
                'reason': 'IEEE Rashtriya Tathyanka Injiniyari Sammelanma pahanako bata sahabhagi hunalai.',
                'status': 'Pending'
            }
        )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with Nepali names (romanized)!"))
