
from django.contrib import admin
from django.urls import path
from school import views
from django.contrib.auth.views import LoginView,LogoutView
from school import views
from school.views import student_lessons_view
from school.views import get_exams
from school.views import exam_history, update_exam, delete_exam
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from school.views import send_email_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),
    path('adminclick', views.adminclick_view),
    path('get_exams/', get_exams, name='get_exams'),
    path('teacherclick', views.teacherclick_view),
    path('student-lessons/', student_lessons_view, name='student_lessons'),
    path('studentclick', views.studentclick_view),
    path('student/lesson/<int:lesson_id>/', views.student_lesson_detail, name='student-lesson-detail'),
    path('teacher/marks/', views.teacher_marks_view, name='teacher-marks'),
    path('teacher/class/<str:grade>/', views.class_students_view, name='class-students'),
    path('get_exams/', views.get_exams, name='get_exams'),
    path('get_exam_marks/', views.get_exam_marks, name='get_exam_marks'),
    path('delete_exam/<int:exam_id>/', views.delete_exam, name='delete_exam'),
    path('exam-history/', exam_history, name='exam_history'),
    path('update-exam/<str:exam_name>/', update_exam, name='update_exam'),
    path('delete-exam/<str:exam_name>/', delete_exam, name='delete_exam'),
    path('send-email/', views.send_email, name='send_email'),
    path('feedback/', views.send_feedback, name='send_feedback'),
    path('contact/', views.send_feedback, name='feedback'),  # ✅ لاحظ اسم `feedback` هنا

    path('add_lesson/', views.add_lesson, name='add_lesson'),
    path('update_teacher/<int:lesson_id>/', views.update_teacher, name='update_teacher'),
    path('delete_lesson/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'),
    path('delete_notice/<int:notice_id>/', views.delete_notice, name='delete_notice'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('adminsignup', views.admin_signup_view),
    path('studentsignup', views.student_signup_view,name='studentsignup'),
    path('teachersignup', views.teacher_signup_view),
    path('adminlogin', LoginView.as_view(template_name='school/adminlogin.html')),
    path('studentlogin', LoginView.as_view(template_name='school/studentlogin.html')),
    path('teacherlogin', LoginView.as_view(template_name='school/teacherlogin.html')),


    path('afterlogin/', views.afterlogin_view, name='afterlogin'),
    path('logout/', LogoutView.as_view(template_name='school/index.html', http_method_names=['get', 'post']), name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),


    path('admin-teacher', views.admin_teacher_view,name='admin-teacher'),
    path('admin-add-teacher', views.admin_add_teacher_view,name='admin-add-teacher'),
    path('admin-view-teacher', views.admin_view_teacher_view,name='admin-view-teacher'),
    path('admin-approve-teacher', views.admin_approve_teacher_view,name='admin-approve-teacher'),
    path('approve-teacher/<int:pk>', views.approve_teacher_view,name='approve-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view,name='delete-teacher'),
    path('delete-teacher-from-school/<int:pk>', views.delete_teacher_from_school_view,name='delete-teacher-from-school'),
    path('update-teacher/<int:pk>', views.update_teacher_view,name='update-teacher'),
    path('admin-view-teacher-salary', views.admin_view_teacher_salary_view,name='admin-view-teacher-salary'),


    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-add-student', views.admin_add_student_view,name='admin-add-student'),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),
    path('delete-student-from-school/<int:pk>', views.delete_student_from_school_view,name='delete-student-from-school'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('admin-approve-student', views.admin_approve_student_view,name='admin-approve-student'),
    path('approve-student/<int:pk>', views.approve_student_view,name='approve-student'),
    path('admin-view-student-fee', views.admin_view_student_fee_view,name='admin-view-student-fee'),


    path('admin-attendance', views.admin_attendance_view,name='admin-attendance'),
    path('admin-take-attendance/<str:cl>', views.admin_take_attendance_view,name='admin-take-attendance'),
    path('admin-view-attendance/<str:cl>', views.admin_view_attendance_view,name='admin-view-attendance'),


    path('admin-fee', views.admin_fee_view,name='admin-fee'),
    path('admin-view-fee/<str:cl>', views.admin_view_fee_view,name='admin-view-fee'),

    path('admin-notice', views.admin_notice_view,name='admin-notice'),



    path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
    path('teacher-attendance', views.teacher_attendance_view,name='teacher-attendance'),
    path('teacher-take-attendance/<str:cl>', views.teacher_take_attendance_view,name='teacher-take-attendance'),
    path('teacher-view-attendance/<str:cl>', views.teacher_view_attendance_view,name='teacher-view-attendance'),
    path('teacher-notice', views.teacher_notice_view,name='teacher-notice'),

    path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),
    path('student-attendance', views.student_attendance_view,name='student-attendance'),

    path('aboutus/', views.aboutus_view, name='aboutus'),


    path('contactus/', views.contactus_view, name='contactus'),

    path('contactus', views.contactus_view),

    path('send-email/', send_email_view, name='send_email'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
