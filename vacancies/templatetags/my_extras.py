from django import template

register = template.Library()


@register.simple_tag
def word_by_number(number, s1, s2, s3, show_number=True):
    s = s3
    remainder = number % 100
    if remainder not in range(5, 20):
        remainder %= 10
        if remainder in (2, 3, 4):
            s = s2
        elif remainder == 1:
            s = s1
    if show_number:
        s = str(number) + " " + s
    return s


@register.simple_tag
def vacancy_by_number(number, show_number=True):
    return word_by_number(number, 'вакансия', 'вакансии', 'вакансий', show_number)


@register.simple_tag
def response_by_number(number, show_number=True, ):
    return word_by_number(number, 'отклик', 'отклика', 'откликов', show_number)


@register.simple_tag
def people_by_number(number, show_number=True, ):
    return word_by_number(number, 'человек', 'человека', 'человек', show_number)


@register.simple_tag
def people_by_number(number, show_number=True, ):
    return word_by_number(number, 'человек', 'человека', 'человек', show_number)
