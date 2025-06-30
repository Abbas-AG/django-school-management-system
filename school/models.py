from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TeacherExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salary = models.PositiveIntegerField(null=False)
    joindate = models.DateField(auto_now_add=True)
    mobile = models.CharField(max_length=40)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

    @property
    def get_id(self):
        return self.user.id

    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


classes=[('one','one'),('two','two'),('three','three'),
('four','four'),('five','five'),('six','six')]
class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    roll = models.CharField(max_length=10)
    mobile = models.CharField(max_length=40,null=True)
    fee=models.PositiveIntegerField(null=True)
    cl= models.CharField(max_length=10,choices=classes,default='one')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name

class Lesson(models.Model):
    GRADE_CHOICES = [
        ('one', 'First Year Intermediate'),
        ('two', 'Second Year Intermediate'),
        ('three', 'Third Year Intermediate'),
        ('four', 'Fourth Year Secondary'),
        ('five', 'Fifth Year Secondary'),
        ('six', 'Sixth Year Secondary'),
    ]


    name = models.CharField(max_length=255)
    description = models.TextField(default="No description")
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES, default="one")
    teacher = models.ForeignKey(
        TeacherExtra,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Teacher"
    )

    def __str__(self):
        return self.name

    def get_grade_display(self):
        return dict(self.GRADE_CHOICES).get(self.grade, '')
class Exam(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentExtra, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=255)
    total_marks = models.PositiveIntegerField()
    obtained_marks = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(TeacherExtra, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.exam_name} - {self.student.get_name}"

class Attendance(models.Model):
    roll=models.CharField(max_length=10,null=True)
    date=models.DateField()
    cl=models.CharField(max_length=10)
    present_status = models.CharField(max_length=10)



class Notice(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,null=True,default='school')
    message=models.CharField(max_length=500)
    image = models.ImageField(upload_to='notices/', null=True, blank=True)  # حقل الصورة
