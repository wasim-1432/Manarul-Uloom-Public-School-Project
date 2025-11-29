from django import template
register = template.Library()

@register.filter
def grade(value):
    try:
        m = float(value)
        if m >= 91: return "A1"
        elif m >= 81: return "A2"
        elif m >= 71: return "B1"
        elif m >= 61: return "B2"
        elif m >= 51: return "C1"
        elif m >= 41: return "C2"
        elif m >= 33: return "D"
        else: return "E"
    except:
        return "E"