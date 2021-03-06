from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL

class MyUser(models.Model):
    choices_list = [
        ('AC', 'Academic'),
        ('SE', 'Secretary'),
        ('TE', 'Teacher'),
    ]
    nm = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    role = models.CharField(max_length=100, choices=choices_list)
    value_key = models.CharField(max_length=100, blank=True, null=True)


class SchoolProfile(models.Model):
    nm = models.ForeignKey(User, on_delete=models.CASCADE)
    name_of_the_school = models.CharField(max_length=50)
    logo_of_the_school = models.ImageField(default='default.png',blank=True, null=True)
    description_of_the_school = models.CharField(max_length=1000, blank=True, null=True)
    address_of_the_school = models.CharField(max_length=50, blank=True, null=True)
    vision_of_the_school = models.CharField(max_length=50, blank=True, null=True)
    motto_of_the_school = models.CharField(max_length=50, blank=True, null=True)
    email_of_the_school = models.EmailField(blank=True, null=True)
    website_of_the_school = models.CharField(max_length=50, blank=True, null=True)
    ch = [
        ('a', 'A level'),
        ('o', 'O level'),
        ('p', 'P level'),
        ('k', 'K level'),
    ]
    school_category = models.CharField(max_length=1, choices=ch, blank=False, null=False)


class Post(models.Model):
    nm = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', blank=False, null=True)
    send_notifications_to_teachers = models.TextField()
    time_sent = models.DateTimeField(blank=True, null=True, auto_now=True)



class Students(models.Model):
    nm = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, default='-')
    last_name = models.CharField(max_length=50)
    candidate_number = models.CharField(max_length=20, blank=True, null=True)
    ch = [('M', 'Male'), ('F', 'Female')]
    sex = models.CharField(max_length=1, choices=ch)
    darasa = models.CharField(max_length=2)

class ClassList(models.Model):
    '''List of all possible classes'''
    nm = models.ForeignKey(User, on_delete=models.CASCADE)
    ol = [
        ('form 1', 'form 1'),
        ('form 2', 'form 2'),
        ('form 3', 'form 3'),
        ('form 4', 'form 4'),
    ]
    al = [
        ('form 5', 'form 5'),
        ('form 6', 'form 6'),
    ]
    pl = [
        ('standard 1', 'standard 1'),
        ('standard 2', 'standard 2'),
        ('standard 3', 'standard 3'),
        ('standard 4', 'standard 4'),
        ('standard 5', 'standard 5'),
        ('standard 6', 'standard 6'),
        ('standard 7', 'standard 7'),
    ]
    kl = [
        ('level 1', 'level 1'),
        ('level 2', 'level 2'),
        ('level 3', 'level 3'),
    ]

    primary_level = models.CharField(max_length=15, choices=pl)
    advanced_level = models.CharField(max_length=15, choices=al)
    ordinary_level = models.CharField(max_length=15, choices=ol)
    k_level = models.CharField(max_length=15, choices=kl)
    contact_your_administrator_to_setup_the_classes_of_your_school = models.CharField(max_length=1)


class SubjectList(models.Model):
    nm = models.ForeignKey(User, on_delete=models.CASCADE)
    name_of_the_subject = models.CharField(max_length=50, null=True, blank=False)


class AcademicBtn(models.Model):
    ch = [
        ('name', 'name of the students'),
        ('number', 'number of the students'),
        ('none', 'Not authorize to access table'),
    ]
    nm = models.ForeignKey(User, on_delete=models.CASCADE)
    type_of_table_to_be_filled_by_teacher = models.CharField(
        max_length=8, choices=ch, default='name')

class AcademicSetup(models.Model):
    nm = models.ForeignKey(User, on_delete=models.CASCADE)
    # Name of the examination
    name_of_the_examination = models.CharField(max_length=100)

    # Grades for the examination
    A = models.IntegerField(default=80)
    B = models.IntegerField(default=70)
    C = models.IntegerField(default=60)
    D = models.IntegerField(default=50)
    E = models.IntegerField(default=40, null=True, blank=False)
    S = models.IntegerField(default=35, null=True, blank=False)
    F = models.IntegerField(default=0)

    # Division points
    division_1 = models.IntegerField(default=9)
    division_2 = models.IntegerField(default=12)
    division_3 = models.IntegerField(default=18)
    division_4 = models.IntegerField(default=22)
    division_0 = models.IntegerField(default=25)


class SecretaryRoles(models.Model):
    nm = models.ForeignKey(User, on_delete=models.CASCADE)

    #defining the fields
    unsorted_results_in_csv = models.BooleanField()
    unsorted_results_in_html = models.BooleanField()
    sorted_results_in_csv = models.BooleanField()
    sorted_results_in_html = models.BooleanField()
    best_students_analysis = models.BooleanField()
    worst_students_analysis = models.BooleanField()
    analysis_of_each_subject = models.BooleanField()
    general_analysis = models.BooleanField()
    graphs_of_performance = models.BooleanField()
    results_of_each_student = models.BooleanField()

class Authorize(models.Model):
    nm = models.ForeignKey(User, on_delete=models.CASCADE)

    # Boolean value for authorization
    authorize_the_results_to_be_printed_by_the_secretary = models.BooleanField(default=False)



class MarksData(models.Model):# have not already used
    nm = models.ForeignKey(User, on_delete=models.CASCADE)

    name_of_the_submited_subject = models.CharField(max_length=50, blank=True, null=True)
    class_of_the_subject = models.CharField(max_length=50, blank=True, null=True)
    name_of_subject_teacher = models.CharField(max_length=50, blank=True, null=True)
    paper_1 = models.CharField(max_length=10, blank=True, null=True)
    paper_2 = models.CharField(max_length=10, blank=True, null=True)
    paper_3 = models.CharField(max_length=10, blank=True, null=True)
    marks = models.CharField(max_length=10000, blank=True, null=True)
    submitted_time = models.CharField(max_length=50, blank=True, null=True)

class TeacherSetup(models.Model):
    nm = models.ForeignKey(User, on_delete=models.CASCADE)

    my_class = models.CharField(max_length=15, blank=True, null=True)
    my_subject = models.CharField(max_length=20, blank=True, null=True)


class Profile(models.Model):
    nm = models.ForeignKey(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50, blank=False, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True, default='-')
    last_name = models.CharField(max_length=50, blank=False, null=True)
    phone_number = models.CharField(max_length=10, blank=False, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    upload_image = models.ImageField(blank=True, null=True, default='blank_profile_picture.png')
    my_email_address = models.EmailField(blank=False, null=True)
    your_facebook_profile = models.URLField(blank=True, null=True)
    your_instagram_profile = models.URLField(blank=True, null=True)
    your_twitter_profile = models.URLField(blank=True, null=True)
    your_linkedin_profile = models.URLField(blank=True, null=True)


class PracticalFormula(models.Model):
    nm = models.ForeignKey(User, on_delete=models.CASCADE)
    ch = [
        ('formula_1', 'formula 1'),
        ('formula_2', 'formula 2'),
        ('formula_3', 'formula 3'),
    ]
    select_the_formula = models.CharField(max_length=10, choices=ch, default='formula_1')

class UploadToAdmin(models.Model):
    nm = models.ForeignKey(User, on_delete=models.CASCADE)
    internal_files = models.FileField(blank=True, null=True)

class IntermediateValue(models.Model):
    nm = models.ForeignKey(User, on_delete=models.CASCADE)
    inter_val = models.CharField(max_length=20, blank=True, null=True)
