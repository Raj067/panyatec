"""newsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
#from django.views.generic.base import TemplateView
from django.contrib.auth.forms import UserCreationForm
from accounts.urls import *
from administrator.urls import *
from teacher.views import (
    teacher_home, teacher_profile,
    teacher_roles, teacher_work,
    teacher_roles_academic_subject,
    teacher_roles_academic_subject_delete,
    teacher_roles_academic_students_delete,
    teacher_work_academic_general_setup,
    teacher_work_academic_generate_table,
    teacher_roles_teacher_confirm,
    teacher_roles_formula)
from homepage.views import main_home, help_page
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_home, name='panyatech homepage'),
    path('help/', help_page, name='help'),

    path('accounts/password/reset/', reset_password, name='reset password'),
    path('accounts/signup/teacher/', signup_page_te, name='signup teacher'),
    path('accounts/signup/administrator/', signup_page_ad, name='signup administrator'),
    path('accounts/login/', login_page, name='login'),
    path('accounts/logout/', logout_page, name='logout'),
    path('accounts/roles/', roles_homepage, name='Roles homepage'),


    path('teacher/', teacher_home, name='teacher home page'),
    path('teacher/profile/', teacher_profile, name='teacher profile'),
    path('teacher/work/', teacher_work, name='teacher work'),
    path('teacher/work/academic/general/setup/', teacher_work_academic_general_setup, name='general setup'),
    path('teacher/work/academic/generate/table/', teacher_work_academic_generate_table, name='generate table'),


    path('teacher/roles/', teacher_roles, name='teacher Roles'),
    path('teacher/roles/formula/', teacher_roles_formula, name='formulas'),
    path('teacher/roles/teacher/confirm/<str:value>', teacher_roles_teacher_confirm, name='confirm'),
    path('teacher/roles/academic/subject/', teacher_roles_academic_subject, name='Subject List'),
    path('teacher/roles/academic/subject/delete/<str:value>', teacher_roles_academic_subject_delete, name='Delete subject'),
    path('teacher/roles/academic/student/delete/<str:first_name>_<str:middle_name>_<str:last_name>_<str:sex>',
         teacher_roles_academic_students_delete, name='Delete student'),



    path('administrator/notifications/', notifications, name='notifications'),
    path('administrator/home/', administrator_home, name='administrator home'),
    path('administrator/users/', administrator_user, name='administrator users'),
    path('administrator/payment/', administrator_payment, name='administrator payment'),
    path('administrator/profile/', administrator_profile, name='administrator profile'),
    path('administrator/results/', administrator_results, name='administrator results'),
    path('administrator/files/', administrator_files, name='administrator files'),

    #path('administrator/', administrator_homepage, name='administrator home page'),
    #path('accounts/', include('allauth.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),

]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
