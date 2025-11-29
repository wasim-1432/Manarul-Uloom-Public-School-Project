# marksapp/admin.py

from django.contrib import admin
from .models import (
    Session, Student, Marks, CoScholasticActivity,
    CoScholasticGrade, ClassSection, Subject
)

# ------------------------------
# BASIC MODEL ADMINS
# ------------------------------

@admin.register(ClassSection)
class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'section']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(CoScholasticActivity)
class CoScholasticActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']


@admin.register(CoScholasticGrade)
class CoScholasticGradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'activity', 'term1_grade', 'term2_grade']
    list_filter = ['activity__category', 'term1_grade', 'term2_grade']
    search_fields = ['student__name', 'activity__name']


# ------------------------------
# CUSTOM MARKS ADMIN
# ------------------------------

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'pt1', 'pt2']

    # Hide subjects already assigned to this student
    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "subject":
            # admin URL se student id read karna
            student_id = request.GET.get("student")

            if student_id:
                # Iss student ke jo subjects pehle se marks me add ho chuke
                assigned = Marks.objects.filter(student_id=student_id)\
                                        .values_list('subject_id', flat=True)

                # Dropdown me unko hide karna
                kwargs["queryset"] = Subject.objects.exclude(id__in=assigned)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ------------------------------
# DIRECT REGISTER BASIC MODELS
# ------------------------------
admin.site.register(Session)
admin.site.register(Student)
