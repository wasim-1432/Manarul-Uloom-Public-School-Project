from django.shortcuts import render
from .models import Student, Marks, CoScholasticGrade

def get_grade(marks):
    m = float(marks)
    if m >= 91: return "A1"
    elif m >= 81: return "A2"
    elif m >= 71: return "B1"
    elif m >= 61: return "B2"
    elif m >= 51: return "C1"
    elif m >= 41: return "C2"
    elif m >= 33: return "D"
    else: return "E"


def enter_roll(request):
    if request.method == "POST":
        roll_no = request.POST.get('roll_no')
        name = request.POST.get('name', '').strip().title()

        try:
            student = Student.objects.get(roll_no=roll_no, name__icontains=name)

            # ✔ Load Scholastic Marks
            marks = Marks.objects.filter(student=student).select_related('subject')

            # ✔ Load & Sort Co-Scholastic Grades by Category (IMPORTANT!)
            coscholastic = (
                CoScholasticGrade.objects
                .filter(student=student)
                .select_related('activity')
                .order_by('activity__category')    # <-- FIXED
            )

            # ✔ Scholastic Calculation
            if marks.exists():
                term1_total = sum(m.term1_total() for m in marks)
                term2_total = sum(m.term2_total() for m in marks)
                final_total = sum(m.final_total() for m in marks)

                term1_percent = round(term1_total / len(marks), 1)
                term2_percent = round(term2_total / len(marks), 1)
                overall_percent = round((term1_percent + term2_percent) / 2, 1)
            else:
                term1_total = term2_total = final_total = 0
                term1_percent = term2_percent = overall_percent = 0

            context = {
                'student': student,
                'marks': marks,
                'coscholastic': coscholastic,
                'term1_total': int(term1_total),
                'term2_total': int(term2_total),
                'term1_percent': term1_percent,
                'term2_percent': term2_percent,
                'overall_percent': overall_percent,
                'term1_grade': get_grade(term1_percent),
                'term2_grade': get_grade(term2_percent),
                'overall_grade': get_grade(overall_percent),
            }

            return render(request, 'marksheet.html', context)

        except Student.DoesNotExist:
            return render(request, 'enter_roll.html', {'error': 'Student not found!'})

    return render(request, 'enter_roll.html')
