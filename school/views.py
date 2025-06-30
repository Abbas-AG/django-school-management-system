from django.shortcuts import render, redirect, reverse, get_object_or_404
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from .models import Notice, Lesson, StudentExtra, TeacherExtra, Exam
from .forms import LessonForm
from django.contrib import messages
import traceback  # لإظهار تفاصيل الأخطاء
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import logging
from .forms import NoticeForm  # تأكد من استيراد الفورم بشكل صحيح
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Feedback
from django.core.mail import EmailMultiAlternatives

def contactus_view(request):
    return render(request, 'school/contactus.html')

def send_feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # حفظ الرسالة في قاعدة البيانات
        Feedback.objects.create(name=name, email=email, message=message)

        subject = 'Thank you for contacting us!'
        from_email = settings.EMAIL_HOST_USER
        to = [email]

        # رسالة نصية عادية كنسخة احتياطية
        text_content = f"Dear {name},\n\nThank you for your message!\n\nWe received:\n\"{message}\"\n\nWe will get back to you soon."

        # رسالة HTML حديثة
        html_content = f"""
        <html>
          <head>
            <style>
              .container {{
                max-width: 600px;
                margin: auto;
                padding: 20px;
                font-family: 'Arial', sans-serif;
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 8px;
              }}
              .header {{
                background-color: #0072ff;
                color: #ffffff;
                padding: 15px;
                text-align: center;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
              }}
              .content {{
                padding: 20px;
                line-height: 1.6;
                color: #333333;
              }}
              .content blockquote {{
                background: #e9ecef;
                border-left: 4px solid #0072ff;
                margin: 20px 0;
                padding: 10px 20px;
                font-style: italic;
              }}
              .footer {{
                text-align: center;
                font-size: 12px;
                color: #777777;
                margin-top: 20px;
              }}
            </style>
          </head>
          <body>
            <div class="container">
              <div class="header">
                <h2>Thank you for contacting us!</h2>
              </div>
              <div class="content">
                <p>Dear {name},</p>
                <p>Thank you for your message!</p>
                <p>We received:</p>
                <blockquote>{message}</blockquote>
                <p>We will get back to you soon.</p>
              </div>
              <div class="footer">
                <p>&copy; 2025 Al-Tamayuz. All rights reserved.</p>
              </div>
            </div>
          </body>
        </html>
        """

        # إرسال البريد بصيغة HTML
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
            print("Email sent successfully to:", email)
        except Exception as e:
            print("Error sending email:", e)

        return render(request, 'school/contactussuccess.html')

    return render(request, 'school/contactus.html')

def add_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'DONE!')
            return redirect('add_lesson')
        else:
            messages.error(request, 'ERROR!')
    else:
        form = LessonForm()

    lessons = Lesson.objects.all()
    teachers = TeacherExtra.objects.all()  # ستعمل الآن بعد التصحيح

    return render(request, 'school/add_lesson.html', {
        'form': form,
        'lessons': lessons,
        'teachers': teachers
    })

def send_email(request):
    if request.method == "POST":
        # هنا يمكنك إضافة الكود لمعالجة الرسالة
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # يمكن إضافة الكود هنا لإرسال البريد الإلكتروني أو حفظ البيانات

        messages.success(request, 'Your message has been sent successfully!')
        return render(request, 'school/contactussuccess.html')

    return render(request, 'school/contactussuccess.html')


def delete_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    lesson.delete()
    messages.success(request, 'DONE!')
    return redirect('add_lesson')


# دالة جديدة لتحديث المدرس
def update_teacher(request, lesson_id):
    if request.method == 'POST':
        lesson = Lesson.objects.get(id=lesson_id)
        teacher_id = request.POST.get('teacher')
        if teacher_id:
            lesson.teacher = TeacherExtra.objects.get(id=teacher_id)
        else:
            lesson.teacher = None
        lesson.save()
        messages.success(request, 'EXAM UPDATED!')
    return redirect('add_lesson')


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'school/index.html')


def delete_notice(request, notice_id):
    # الحصول على المنشور المحدد
    notice = get_object_or_404(Notice, id=notice_id)
    # حذف المنشور
    notice.delete()


#for showing signup/login button for teacher(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'school/adminclick.html')


def admin_dashboard(request):
    # استرجاع الإشعارات المتبقية
    notice = Notice.objects.all(
    )  # أو يمكنك إضافة فلاتر لتحديد الإشعارات المعروضة
    return render(request, 'school/admin_dashboard.html', {'notice': notice})


#for showing signup/login button for teacher(by sumit)
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'school/teacherclick.html')


#for showing signup/login button for student(by sumit)
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'school/studentclick.html')


def admin_signup_view(request):
    form = forms.AdminSigupForm()
    if request.method == 'POST':
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request, 'school/adminsignup.html', {'form': form})


def student_signup_view(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request, 'school/studentsignup.html', context=mydict)


def teacher_signup_view(request):
    form1 = forms.TeacherUserForm()
    form2 = forms.TeacherExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.TeacherUserForm(request.POST)
        form2 = forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('teacherlogin')
    return render(request, 'school/teachersignup.html', context=mydict)


#for checking user is techer , student or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_teacher(request.user):
        accountapproval = models.TeacherExtra.objects.all().filter(
            user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('teacher-dashboard')
        else:
            return render(request, 'school/teacher_wait_for_approval.html')
    elif is_student(request.user):
        accountapproval = models.StudentExtra.objects.all().filter(
            user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('student-dashboard')
        else:
            return render(request, 'school/student_wait_for_approval.html')


#for dashboard of adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn(by sumit)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount = models.TeacherExtra.objects.all().filter(
        status=True).count()
    pendingteachercount = models.TeacherExtra.objects.all().filter(
        status=False).count()

    studentcount = models.StudentExtra.objects.all().filter(
        status=True).count()
    pendingstudentcount = models.StudentExtra.objects.all().filter(
        status=False).count()

    teachersalary = models.TeacherExtra.objects.filter(status=True).aggregate(
        Sum('salary'))
    pendingteachersalary = models.TeacherExtra.objects.filter(
        status=False).aggregate(Sum('salary'))

    studentfee = models.StudentExtra.objects.filter(status=True).aggregate(
        Sum('fee', default=0))
    pendingstudentfee = models.StudentExtra.objects.filter(
        status=False).aggregate(Sum('fee'))

    notice = models.Notice.objects.all()

    #aggregate function return dictionary so fetch data from dictionay(by sumit)
    mydict = {
        'teachercount': teachercount,
        'pendingteachercount': pendingteachercount,
        'studentcount': studentcount,
        'pendingstudentcount': pendingstudentcount,
        'teachersalary': teachersalary['salary__sum'],
        'pendingteachersalary': pendingteachersalary['salary__sum'],
        'studentfee': studentfee['fee__sum'],
        'pendingstudentfee': pendingstudentfee['fee__sum'],
        'notice': notice
    }

    return render(request, 'school/admin_dashboard.html', context=mydict)


#for teacher sectionnnnnnnn by adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn(by sumit)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_teacher_view(request):
    return render(request, 'school/admin_teacher.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_teacher_view(request):
    form1 = forms.TeacherUserForm()
    form2 = forms.TeacherExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.TeacherUserForm(request.POST)
        form2 = forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()

            f2 = form2.save(commit=False)
            f2.user = user
            f2.status = True
            f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-teacher')
    return render(request, 'school/admin_add_teacher.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_view(request):
    teachers = models.TeacherExtra.objects.all().filter(status=True)
    return render(request, 'school/admin_view_teacher.html',
                  {'teachers': teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_teacher_view(request):
    teachers = models.TeacherExtra.objects.all().filter(status=False)
    return render(request, 'school/admin_approve_teacher.html',
                  {'teachers': teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_teacher_view(request, pk):
    teacher = models.TeacherExtra.objects.get(id=pk)
    teacher.status = True
    teacher.save()
    return redirect(reverse('admin-approve-teacher'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_view(request, pk):
    teacher = models.TeacherExtra.objects.get(id=pk)
    user = models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-approve-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_from_school_view(request, pk):
    teacher = models.TeacherExtra.objects.get(id=pk)
    user = models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-view-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_teacher_view(request, pk):
    teacher = models.TeacherExtra.objects.get(id=pk)
    user = models.User.objects.get(id=teacher.user_id)

    form1 = forms.TeacherUserForm(instance=user)
    form2 = forms.TeacherExtraForm(instance=teacher)
    mydict = {'form1': form1, 'form2': form2}

    if request.method == 'POST':
        form1 = forms.TeacherUserForm(request.POST, instance=user)
        form2 = forms.TeacherExtraForm(request.POST, instance=teacher)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.status = True
            f2.save()
            return redirect('admin-view-teacher')
    return render(request, 'school/admin_update_teacher.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_salary_view(request):
    teachers = models.TeacherExtra.objects.all()
    return render(request, 'school/admin_view_teacher_salary.html',
                  {'teachers': teachers})


#for student by adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn(by sumit)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request, 'school/admin_student.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            print("form is valid")
            user = form1.save()
            user.set_password(user.password)
            user.save()

            f2 = form2.save(commit=False)
            f2.user = user
            f2.status = True
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-student')
    return render(request, 'school/admin_add_student.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_view(request):
    students = models.StudentExtra.objects.all().filter(status=True)
    return render(request, 'school/admin_view_student.html',
                  {'students': students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_from_school_view(request, pk):
    student = models.StudentExtra.objects.get(id=pk)
    user = models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_view(request, pk):
    student = models.StudentExtra.objects.get(id=pk)
    user = models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-approve-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_student_view(request, pk):
    student = models.StudentExtra.objects.get(id=pk)
    user = models.User.objects.get(id=student.user_id)
    form1 = forms.StudentUserForm(instance=user)
    form2 = forms.StudentExtraForm(instance=student)
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST, instance=user)
        form2 = forms.StudentExtraForm(request.POST, instance=student)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.status = True
            f2.save()
            return redirect('admin-view-student')
    return render(request, 'school/admin_update_student.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_student_view(request):
    students = models.StudentExtra.objects.all().filter(status=False)
    return render(request, 'school/admin_approve_student.html',
                  {'students': students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_student_view(request, pk):
    students = models.StudentExtra.objects.get(id=pk)
    students.status = True
    students.save()
    return redirect(reverse('admin-approve-student'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_fee_view(request):
    students = models.StudentExtra.objects.all()
    return render(request, 'school/admin_view_student_fee.html',
                  {'students': students})


#attendance related viewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww(by sumit)
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_attendance_view(request):
    return render(request, 'school/admin_attendance.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_take_attendance_view(request, cl):
    students = models.StudentExtra.objects.all().filter(cl=cl)
    print(students)
    aform = forms.AttendanceForm()
    if request.method == 'POST':
        form = forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances = request.POST.getlist('present_status')
            date = form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel = models.Attendance()
                AttendanceModel.cl = cl
                AttendanceModel.date = date
                AttendanceModel.present_status = Attendances[i]
                AttendanceModel.roll = students[i].roll
                AttendanceModel.save()
            return redirect('admin-attendance')
        else:
            print('form invalid')
    return render(request, 'school/admin_take_attendance.html', {
        'students': students,
        'aform': aform
    })


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_attendance_view(request, cl):
    form = forms.AskDateForm()
    if request.method == 'POST':
        form = forms.AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            attendancedata = models.Attendance.objects.all().filter(date=date,
                                                                    cl=cl)
            studentdata = models.StudentExtra.objects.all().filter(cl=cl)
            mylist = zip(attendancedata, studentdata)
            return render(request, 'school/admin_view_attendance_page.html', {
                'cl': cl,
                'mylist': mylist,
                'date': date
            })
        else:
            print('form invalid')
    return render(request, 'school/admin_view_attendance_ask_date.html', {
        'cl': cl,
        'form': form
    })


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_fee_view(request):
    return render(request, 'school/admin_fee.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_fee_view(request, cl):
    feedetails = models.StudentExtra.objects.all().filter(cl=cl)
    return render(request, 'school/admin_view_fee.html', {
        'feedetails': feedetails,
        'cl': cl
    })


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_notice_view(request):
    form = NoticeForm()
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)  # إضافة request.FILES لاستقبال الملفات
        if form.is_valid():
            notice = form.save(commit=False)
            notice.by = request.user.first_name
            notice.save()
            return redirect('admin-dashboard')
    return render(request, 'school/admin_notice.html', {'form': form})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacherdata = models.TeacherExtra.objects.all().filter(
        status=True, user_id=request.user.id)
    notice = models.Notice.objects.all()
    mydict = {
        'salary': teacherdata[0].salary,
        'mobile': teacherdata[0].mobile,
        'date': teacherdata[0].joindate,
        'notice': notice
    }
    return render(request, 'school/teacher_dashboard.html', context=mydict)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_attendance_view(request):
    return render(request, 'school/teacher_attendance.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_take_attendance_view(request, cl):
    students = models.StudentExtra.objects.all().filter(cl=cl)
    aform = forms.AttendanceForm()
    if request.method == 'POST':
        form = forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances = request.POST.getlist('present_status')
            date = form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel = models.Attendance()
                AttendanceModel.cl = cl
                AttendanceModel.date = date
                AttendanceModel.present_status = Attendances[i]
                AttendanceModel.roll = students[i].roll
                AttendanceModel.save()
            return redirect('teacher-attendance')
        else:
            print('form invalid')
    return render(request, 'school/teacher_take_attendance.html', {
        'students': students,
        'aform': aform
    })


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_attendance_view(request, cl):
    form = forms.AskDateForm()
    if request.method == 'POST':
        form = forms.AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            attendancedata = models.Attendance.objects.all().filter(date=date,
                                                                    cl=cl)
            studentdata = models.StudentExtra.objects.all().filter(cl=cl)
            mylist = zip(attendancedata, studentdata)
            return render(request, 'school/teacher_view_attendance_page.html',
                          {
                              'cl': cl,
                              'mylist': mylist,
                              'date': date
                          })
        else:
            print('form invalid')
    return render(request, 'school/teacher_view_attendance_ask_date.html', {
        'cl': cl,
        'form': form
    })


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_notice_view(request):
    form = NoticeForm()
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)  # تأكد من تضمين request.FILES
        if form.is_valid():
            notice = form.save(commit=False)
            notice.by = request.user.first_name  # يمكنك تخصيص هذا حسب الحاجة
            notice.save()
            return redirect('teacher-dashboard')
        else:
            print('form invalid')
    return render(request, 'school/teacher_notice.html', {'form': form})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    studentdata = models.StudentExtra.objects.all().filter(
        status=True, user_id=request.user.id)
    notice = models.Notice.objects.all()
    mydict = {
        'roll': studentdata[0].roll,
        'mobile': studentdata[0].mobile,
        'fee': studentdata[0].fee,
        'notice': notice
    }
    return render(request, 'school/student_dashboard.html', context=mydict)


def student_lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    student = StudentExtra.objects.get(user=request.user)
    exams = Exam.objects.filter(lesson=lesson, student=student)
    return render(request, 'school/student_lesson_detail.html', {
        'lesson': lesson,
        'exams': exams
    })


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_marks_view(request):
    teacher = get_object_or_404(TeacherExtra, user=request.user)
    classes = Lesson.objects.filter(teacher=teacher).values('grade').distinct()
    return render(request, 'school/teacher_marks.html', {
        'teacher': teacher,
        'classes': classes
    })


def get_exams(request):
    lesson_id = request.GET.get('lesson_id')
    if not lesson_id:
        return JsonResponse({'error': 'Lesson ID is required'}, status=400)

    exams = Exam.objects.filter(lesson_id=lesson_id).values(
        'id', 'exam_name', 'date_created')
    exams_list = []
    for exam in exams:
        students_marks = Exam.objects.filter(id=exam['id']).values(
            'student__id', 'obtained_marks')
        exam['students_marks'] = list(students_marks)
        exams_list.append(exam)

    return JsonResponse({'exams': exams_list})


# جلب درجات الامتحان
def get_exam_marks(request):
    exam_id = request.GET.get("exam_id")
    if not exam_id:
        return JsonResponse({"error": "EXAM IS NOT SET!"},
                            status=400)

    marks = Exam.objects.filter(id=exam_id).values('student__id',
                                                   'obtained_marks')
    return JsonResponse({"marks": list(marks)})


@require_http_methods(["DELETE"])
def delete_exam(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
        exam.delete()
        return JsonResponse({'status': 'success'})
    except Exam.DoesNotExist:
        return JsonResponse({'error': 'Exam not found'}, status=404)
def exam_history(request):
    exams = Exam.objects.values('exam_name').distinct()  # إحضار أسماء الامتحانات فقط

    selected_exam_name = request.GET.get('exam_name')
    exam_results = None

    if selected_exam_name:
        exam_results = Exam.objects.filter(exam_name=selected_exam_name)  # جلب جميع الطلاب ودرجاتهم لهذا الامتحان

    context = {
        'exams': exams,
        'selected_exam_name': selected_exam_name,
        'exam_results': exam_results,
    }
    return render(request, 'school/exam_history.html', context)
def delete_exam(request, exam_name):
    if request.method == 'POST':
        exams = Exam.objects.filter(exam_name=exam_name)
        if exams.exists():
            exams.delete()
            messages.success(request, f'DELEATED"{exam_name}"!')
        else:
            messages.error(request, 'THIS EXAM DOES NOT EXEST')
    return redirect('exam_history')

def update_exam(request, exam_name):
    if request.method == 'POST':
        exams = Exam.objects.filter(exam_name=exam_name)
        total_marks = request.POST.get('total_marks')

        for exam in exams:
            obtained_marks = request.POST.get(f'marks_{exam.student.id}')
            if obtained_marks is not None:
                exam.obtained_marks = int(obtained_marks)
                exam.total_marks = int(total_marks) if total_marks else exam.total_marks
                exam.save()

    return exam_history(request)  # إعادة التوجيه إلى نفس الصفحة بعد التحديث

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def class_students_view(request, grade):
    teacher = get_object_or_404(TeacherExtra, user=request.user)
    students = StudentExtra.objects.filter(cl=grade)
    lessons = Lesson.objects.filter(teacher=teacher, grade=grade)

    if request.method == 'POST':
        lesson_id = request.POST.get('lesson')
        exam_id = request.POST.get('exam_id')
        exam_name = request.POST.get('exam_name')
        total_marks = request.POST.get('total_marks')

        lesson = get_object_or_404(Lesson, id=lesson_id)

        for student in students:
            obtained = request.POST.get(f'marks_{student.id}')
            if obtained:
                Exam.objects.update_or_create(lesson=lesson,
                                              student=student,
                                              exam_name=exam_name,
                                              defaults={
                                                  'total_marks': total_marks,
                                                  'obtained_marks': obtained,
                                                  'teacher': teacher
                                              })
        return redirect('class-students', grade=grade)

    return render(request, 'school/class_students.html', {
        'students': students,
        'lessons': lessons,
        'grade': grade
    })


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_attendance_view(request):
    form = forms.AskDateForm()
    if request.method == 'POST':
        form = forms.AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            studentdata = models.StudentExtra.objects.all().filter(
                user_id=request.user.id, status=True)
            attendancedata = models.Attendance.objects.all().filter(
                date=date, cl=studentdata[0].cl, roll=studentdata[0].roll)
            mylist = zip(attendancedata, studentdata)
            return render(request, 'school/student_view_attendance_page.html',
                          {
                              'mylist': mylist,
                              'date': date
                          })
        else:
            print('form invalid')
    return render(request, 'school/student_view_attendance_ask_date.html',
                  {'form': form})


def student_lessons_view(request):
    try:
        student = StudentExtra.objects.get(user=request.user)
        lessons = Lesson.objects.filter(grade=student.cl)
    except StudentExtra.DoesNotExist:
        lessons = []

    return render(request, 'school/studentlessons.html', {'lessons': lessons})


# for aboutus and contact ussssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss (by sumit)
def aboutus_view(request):
    return render(request, 'school/aboutus.html')


def student_lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    student = StudentExtra.objects.get(user=request.user)
    exams = Exam.objects.filter(lesson=lesson, student=student)
    return render(request, 'school/student_lesson_detail.html', {
        'lesson': lesson,
        'exams': exams
    })


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name) + ' || ' + str(email),
                      message,
                      settings.EMAIL_HOST_USER,
                      settings.EMAIL_RECEIVING_USER,
                      fail_silently=False)
            return render(request, 'school/contactussuccess.html')
    return render(request, 'school/contactus.html', {'form': sub})
    
def send_email_view(request):
    if request.method == 'POST':
        recipient_email = request.POST.get('email')  # Ensure your form has a field named 'email'
        subject = "Welcome to Al-Tamayuz School"
        message = "Thank you for reaching out to us. We will get back to you soon."

        if recipient_email:
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,  # Sender email
                    [recipient_email],  # Recipient email
                    fail_silently=False,
                )
                messages.success(request, "Email sent successfully!")
            except Exception as e:
                messages.error(request, f"Error sending email: {str(e)}")

        return redirect('send_email')  # Change to the correct template

    return render(request, 'school/send_html.html')