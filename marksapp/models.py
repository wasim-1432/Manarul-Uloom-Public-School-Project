# marksapp/models.py
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from django.db import models

class Session(models.Model):
    session = models.CharField(max_length=9)
    def __str__(self): return self.session

class ClassSection(models.Model):
    class_name = models.CharField(max_length=10)
    section = models.CharField(max_length=5)
    def __str__(self): return f"{self.class_name} - {self.section}"

class Subject(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self): return self.name

class Student(models.Model):
    roll_no = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    fathers_name = models.CharField(max_length=100, blank=True)
    mothers_name = models.CharField(max_length=100, blank=True)
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    def __str__(self): return f"{self.roll_no} - {self.name}"

# Scholastic Marks
class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    pt1 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    notebook_t1 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    sub_enrich_t1 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    half_yearly = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(80)])
    pt2 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    notebook_t2 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    sub_enrich_t2 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    annual = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(80)])

    def clean(self):
        if not (0 <= self.pt1 <= 10):
            raise ValidationError({'pt1': "PT1 must be between 1 and 10."})
        if not (0<=self.notebook_t1<=5):
            raise ValidationError({'notebook_t1': "Notebook T1 must be between 0 and 5."})
        
        if not (0<=self.sub_enrich_t1<=5):
            raise ValidationError({'sub_enrich_t1': "Sub Enrich T1 must be between 0 and 5."})
        
        if not (0<=self.half_yearly<=80):
            raise ValidationError({'half_yearly': "Half Yearly must be between 0 and 80."})
        
        if not (0 <= self.pt2 <= 10):
            raise ValidationError({'pt1': "PT1 must be between 1 and 10."})
        if not (0<=self.notebook_t2<=5):
            raise ValidationError({'notebook_t2': "Notebook T2 must be between 0 and 5."})
        
        if not (0<=self.sub_enrich_t2<=5):
            raise ValidationError({'sub_enrich_t2': "Sub Enrich T2 must be between 0 and 5."})
        
        if not (0<=self.annual<=80):
            raise ValidationError({'annual': "Annual must be between 0 and 80."})
        

    def save(self, *args, **kwargs):
        self.full_clean()   # Validators + clean() always run
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('student', 'subject')


    def term1_total(self): return self.pt1 + self.notebook_t1 + self.sub_enrich_t1 + self.half_yearly
    def term2_total(self): return self.pt2 + self.notebook_t2 + self.sub_enrich_t2 + self.annual
    def final_total(self): return round((self.term1_total() + self.term2_total()) / 2, 1)

# Co-Scholastic & Discipline
class CoScholasticActivity(models.Model):
    CATEGORY_CHOICES = [
        ('2A', 'Part 2(A): Co-Scholastic Activities(To be assessed on a 3 point scale)'),
        ('2B', 'Part 2(B): Health & Physical Education (To be assessed on a 3 point scale)'),
        ('3',  'Part 3: Discipline')
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.get_category_display()} - {self.name}"
    

# Grades of student for each activity
class CoScholasticGrade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity = models.ForeignKey(CoScholasticActivity, on_delete=models.CASCADE)

    term1_grade = models.CharField(
        max_length=1,
        choices=[('A','A'),('B','B'),('C','C')],
        default='B'
    )
    term2_grade = models.CharField(
        max_length=1,
        choices=[('A','A'),('B','B'),('C','C')],
        default='B'
    )

    class Meta:
        unique_together = ('student', 'activity')   # ✔ SAME ACTIVITY duplicate na ho

    def __str__(self):
        return f"{self.student.name} - {self.activity.name}"