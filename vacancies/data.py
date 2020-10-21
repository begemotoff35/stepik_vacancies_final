""" Вакансии """

jobs = [

    {"title": "Разработчик на Python", "cat": "backend", "company": "staffingsmarter", "salary_from": "100000",
     "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Разработчик в проект на Django", "cat": "backend", "company": "swiftattack", "salary_from": "80000",
     "salary_to": "90000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Разработчик на Swift в аутсорс компанию", "cat": "backend", "company": "swiftattack",
     "salary_from": "120000", "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Мидл программист на Python", "cat": "backend", "company": "workiro", "salary_from": "80000",
     "salary_to": "90000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Питонист в стартап", "cat": "backend", "company": "primalassault", "salary_from": "120000",
     "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"}

]

""" Компании """

companies = [

    {"title": "workiro", "location": "Москва", "logo": "logo1.png", "description": "Воркиро", "employee_count": 35},
    {"title": "rebelrage",
     "location": "Санкт-Петербург", "logo": "logo2.png", "description": "Ребелрэдж", "employee_count": 22},
    {"title": "staffingsmarter",
     "location": "Омск", "logo": "logo3.png", "description": "Стаффингмастер", "employee_count": 66},
    {"title": "evilthreat",
     "location": "Санкт-Петербург", "logo": "logo4.png", "description": "Эвилсрет", "employee_count": 45},
    {"title": "hirey",
     "location": "Нижний-Новгород", "logo": "logo5.png", "description": "Хирей", "employee_count": 98},
    {"title": "swiftattack",
     "location": "Рига", "logo": "logo6.png", "description": "Свифтатак", "employee_count": 8},
    {"title": "troller",
     "location": "Смоленск", "logo": "logo7.png", "description": "Троллер", "employee_count": 12},
    {"title": "primalassault",
     "location": "Воронеж", "logo": "logo8.png", "description": "Прималасаут", "employee_count": 78}

]

""" Категории """

specialties = [

    {"code": "frontend", "title": "Фронтенд", "picture": "specialties/specty_frontend.png"},
    {"code": "backend", "title": "Бэкенд", "picture": "specialties/specty_backend.png"},
    {"code": "gamedev", "title": "Геймдев", "picture": "specialties/specty_gamedev.png"},
    {"code": "devops", "title": "Девопс", "picture": "specialties/specty_devops.png"},
    {"code": "design", "title": "Дизайн", "picture": "specialties/specty_design.png"},
    {"code": "products", "title": "Продукты", "picture": "specialties/specty_products.png"},
    {"code": "management", "title": "Менеджмент", "picture": "specialties/specty_management.png"},
    {"code": "testing", "title": "Тестирование", "picture": "specialties/specty_testing.png"}

]

""" Статусы в формате Enum """

#
#
# class EducationChoices(Enum):
#     missing = 'Отсутствует'
#     secondary = 'Среднее'
#     vocational = 'Средне-специальное'
#     incomplete_higher = 'Неполное высшее'
#     higher = 'Высшее'
#
#
# class GradeChoices(Enum):
#     intern = 'intern'
#     junior = 'junior'
#     middle = 'middle'
#     senior = 'senior'
#     lead = 'lead'
#
#
# class SpecialtyChoices(Enum):
#     frontend = 'Фронтенд'
#     backend = 'Бэкенд'
#     gamedev = 'Геймдев'
#     devops = 'Девопс'
#     design = 'Дизайн'
#     products = 'Продукты'
#     management = 'Менеджмент'
#     testing = 'Тестирование'
#
#
# class WorkStatusChoices(Enum):
#     not_in_search = 'Не ищу работу'
#     consideration = 'Рассматриваю предложения'
#     in_search = 'Ищу работу'
