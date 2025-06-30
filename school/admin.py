from django.contrib import admin
from .models import Attendance,StudentExtra,TeacherExtra,Notice
from .models import Feedback

# Register your models here. (by sumit.luv)
class StudentExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentExtra, StudentExtraAdmin)

class TeacherExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(TeacherExtra, TeacherExtraAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attendance, AttendanceAdmin)

class NoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notice, NoticeAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    list_filter = ['created_at']
    search_fields = ('name', 'email', 'message')

admin.site.register(Feedback, FeedbackAdmin)
