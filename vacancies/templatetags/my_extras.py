from django import template

register = template.Library()


@register.simple_tag
def vacancy_by_number(number, show_number=True):
    s = "вакансий"
    remainder = number % 100
    if remainder not in range(5, 20):
        remainder %= 10
        if remainder in (2, 3, 4):
            s = "вакансии"
        elif remainder == 1:
            s = "вакансия"
    if show_number:
        s = str(number) + " " + s
    return s

