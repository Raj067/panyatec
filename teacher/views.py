import numpy as np
import time
from algorithims.front import *
from algorithims.decoretor import *
from algorithims.back import *
from algorithims.formula import *
from algorithims.grades import *
from administrator.models import *
from administrator.forms import *
from django.shortcuts import render, redirect
from .form import RequiredKeyForm
from .models import RequiredKey



def image_show(request, req_pk):
    try:
        image = SchoolProfile.objects.all().filter(nm_id=req_pk)
        image = [i.logo_of_the_school for i in image][0]
        return image.url
    except:
        return None

def name_school_show(request, req_pk):
    try:
        name = SchoolProfile.objects.all().filter(nm_id=req_pk)
        name = [i.name_of_the_school for i in name][0]
        return name
    except:
        return None

def grade_func(request, req_pk, list_of_marks, name, list_of_subject, sex, darasa,
               class_of_the_student):
    data = AcademicSetup.objects.filter(nm_id=req_pk)
    data = [[i.name_of_the_examination, i.A, i.B, i.C,
             i.D, i.E, i.S, i.F, i.division_1,
             i.division_2, i.division_3, i.division_4, i.division_0
             ] for i in data][0]
    d = Grade(A=data[1], B=data[2], C=data[3], D=data[4], E=data[5],
              S=data[6], F=data[7], div_1=data[8], div_2=data[9],
              div_3=data[10], div_4=data[11], div_0=data[12],
              list_of_marks=list_of_marks, name=name,
              list_of_subject=list_of_subject, sex=sex,
              darasa=darasa,  type_of_exam=data[0],
              class_of_students=class_of_the_student,
              name_of_school=name_school_show(request, req_pk))
    return d

@authenticated_te
def teacher_home(request, *args, **kwargs):
    txt = 0
    form = RequiredKeyForm(request.POST or None)
    if form.is_valid():
        val = form.cleaned_data['user_key']
        if validate_key(val):
            reg = RequiredKey(user_key=val, id=request.user.id)
            reg.save()
        else:
            txt = 'The key you have entered is incorrect'

    req = [i.user_key for i in RequiredKey.objects.filter(id=request.user.id)]

    if req == []:
        req = 0
    else:
        req = 1

    info_school = None
    req_role = None
    notifications = None
    req_pk = None
    try:# Try if the data exist in the database
        # his own key so as to get the admin pk -- nm
        data_key = RequiredKey.objects.filter(id=request.user.id)
        # using admin pk
        req_role, req_pk = required_key([i.user_key for i in data_key][0])

        # Using the profile of the school
        info_school = SchoolProfile.objects.all().filter(nm_id=req_pk)
        info_school = [[i.name_of_the_school, i.address_of_the_school,
                    i.email_of_the_school, i.website_of_the_school,
                    i.vision_of_the_school, i.motto_of_the_school,
                    i.description_of_the_school]
                    for i in info_school]
        info_school = np.array(info_school).reshape(7)
    except:
        pass

    post_form = PostForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        post_form.is_valid()
        if post_form.clean():
            notif = post_form.cleaned_data['send_notifications_to_teachers']
            reg_data = Post(send_notifications_to_teachers=notif,
                            sender=request.user, nm_id=req_pk)
            reg_data.save()

    notifications = Post.objects.all().filter(nm_id=req_pk)
    try:  # for notifications
        sender = [i.sender for i in notifications]
        tm = [i.time_sent for i in notifications]
        notifications = [i.send_notifications_to_teachers for i in notifications]

        if notifications == []:
            notifications = 'No notification now'
    except:
        notifications = None
        sender = None
    try:
        my_pic = Profile.objects.filter(nm_id=req_pk, id=request.user.id)
        my_pic = [i.upload_image.url for i in my_pic]
    except:
        my_pic = [None]
    #print(Profile.objects.filter(nm_id=req_pk, id=request.user.id))
    image = image_show(request=request, req_pk=req_pk)
    data = zip(sender, tm, notifications)
    p = [[i, j, k] for i, j, k in data][::-1]
    dt = {
        'req_key': req,
        'form': form,
        'txt': txt,
        'info_school': info_school,
        'req_role': encode(req_role),
        'notifications': notifications,
        'sender': sender,
        'image': image,
        'my_data': p,
        'post_form': post_form,

    }
    return render(request, 'teacher_homepage.html', dt)

@authenticated_te
def teacher_profile(request, *args, **kwargs):

    txt = 0
    try:
        # his own key so as to get the admin pk -- nm
        data_key = RequiredKey.objects.filter(id=request.user.id)
        # using admin pk
        req_role, req_pk = required_key([i.user_key for i in data_key][0])
    except:
        req_role = None
        req_pk = None
        data_key = None

    form = ProfileForm(request.POST or None)
    if request.method == 'POST':
        print('rajabu')
        form = ProfileForm(request.POST, request.FILES)
        form.is_valid()
        if form.clean():
            fname = form.cleaned_data['first_name']
            middle_name = form.cleaned_data['middle_name']
            phone = form.cleaned_data['phone_number']
            last_name = form.cleaned_data['last_name']
            bio = form.cleaned_data['bio']
            upload_image = form.cleaned_data['upload_image']
            my_email_address = form.cleaned_data['my_email_address']
            your_facebook_profile = form.cleaned_data['your_facebook_profile']
            your_instagram_profile = form.cleaned_data['your_instagram_profile']
            your_twitter_profile = form.cleaned_data['your_twitter_profile']
            your_linkedin_profile = form.cleaned_data['your_linkedin_profile']
            reg = Profile(id=request.user.id,
                          nm_id=req_pk,
                          first_name=fname,
                          middle_name=middle_name,
                          last_name=last_name,
                          bio=bio,
                          phone_number=phone,
                          upload_image=upload_image,
                          my_email_address=my_email_address,
                          your_facebook_profile=your_facebook_profile,
                          your_instagram_profile=your_instagram_profile,
                          your_twitter_profile=your_twitter_profile,
                          your_linkedin_profile=your_linkedin_profile,
                          )
            reg.save()
            print(reg)
            txt = 'You have successful updated your profile'

    obj = None
    req_obj = []
    try:
        obj = Profile.objects.filter(id=request.user.id, nm_id=req_pk)

        req_obj = [[i.first_name, i.middle_name,
                    i.phone_number, i.bio]
                   for i in obj]
        # where  total no of fields is 4
        req_obj = np.array(req_obj).reshape(4)

    except:
        pass

    try:
        info = Profile.objects.filter(id=request.user.id, nm_id=req_pk)
        my_name = [[str(i.first_name) + ' ' + str(i.middle_name) + ' ' +
                    str(i.last_name)]
                   for i in info][0][0]
        phone_number = [i.phone_number for i in info][0]
        my_email = [i.my_email_address for i in info][0]
        my_image = [i.upload_image for i in info][0]
        my_image = my_image.url
        my_bio = [i.bio for i in info][0]
        linkedin = [i.your_linkedin_profile for i in info][0]

        facebook = [i.your_facebook_profile for i in info][0]
        twitter = [i.your_twitter_profile for i in info][0]
        instagram = [i.your_instagram_profile for i in info][0]

    except:
        my_name = None
        phone_number = None
        my_email = None
        my_bio = None
        linkedin = None
        facebook = None
        twitter = None
        instagram = None
        my_image = None

    image = image_show(request=request, req_pk=req_pk)
    nschool = name_school_show(request=request, req_pk=req_pk)
    print(my_image)
    dt = {
        'form': form,
        'txt': txt,
        'req_obj': req_obj,
        'obj': obj,
        'data_key': data_key,
        'image': image,
        'nschool': nschool,
        'my_name': my_name,
        'phone_number': phone_number,
        'my_email': my_email,
        'my_bio': my_bio,
        'linkedin': linkedin,
        'facebook' : facebook,
        'twitter': twitter,
        'instagram': instagram,
        'my_image': my_image,


    }
    return render(request, 'teacher_profile.html', dt)

@authenticated_te
def teacher_roles(request, *args, **kwargs):
    txt1 = 0
    txt2 = 0
    nschool = None
    req_role = 0
    product_type = None
    req_pk = None
    data_list = None
    authorize = []

    try:
        # his own key
        data_key = RequiredKey.objects.filter(id=request.user.id)
        # using admin pk
        req_role, req_pk = required_key([i.user_key for i in data_key][0])
    except:
        pass


    # ============================ ALL FORMS ============================== #
    first_form = StudentsForm()  # ACADEMIC
    marks_form = MarksForm()  # TEACHER
    class_form = ClassListForm()  # ACADEMIC

    # ===========================FOR ACADEMIC=============================== #
    if req_role == 'AC':
        # For all form
        first_form = StudentsForm(request.POST or None)  # ACADEMIC
        class_form = ClassListForm(request.POST or None)  # ACADEMIC
        if request.method == 'POST':
            # Class form
            first_form.is_valid()
            txt1 = 'You have successfully add new student to the database'

            # first form
            first_name = first_form.cleaned_data['first_name']
            middle_name = first_form.cleaned_data['middle_name']
            last_name = first_form.cleaned_data['last_name']
            candidate_number = first_form.cleaned_data['candidate_number']
            sex = first_form.cleaned_data['sex']

            # Class form
            class_form.is_valid()
            try:
                darasa = list(class_form.cleaned_data.values())[0]
            except:
                darasa = None
            #User used as nm
            reg = Students(first_name=first_name,
                           middle_name=middle_name,
                           last_name=last_name,
                           candidate_number=candidate_number,
                           sex=sex,
                           darasa=darasa,
                           nm_id=req_pk)
            if darasa != None:
                reg.save()
            else:
                txt1 = 'Contacts your administrator to setup the classes of ' \
                       'your school so as to start saving students to the database'


    # ===========================FOR SECRETARY=============================== #
    files_upload = None
    if req_role == 'SE':
        files_upload = UploadToAdmin.objects.filter(nm_id=req_pk)
        files_upload = [i.internal_files for i in files_upload][::-1]

    # ===========================FOR TEACHER=============================== #
    tea_form = None
    submited_marks = None
    darasa = None
    formula_display = None


    if req_role == 'TE':
        # Type of the product
        try:
            '''
            Academic setup academicbtn with his id so as to avoid duplicate
            while teacher access it without using his or her id
            '''
            tea_form = AcademicBtn.objects.filter(nm_id=req_pk)
            tea_form = [i.type_of_table_to_be_filled_by_teacher for i in tea_form][0]
        except:
            pass
        if tea_form not in ['number', 'name']:
            tea_form = None
        ## Type of formula to display
        try:
            formula_display = PracticalFormula.objects.filter(nm_id=req_pk, id=request.user.id)
            formula_display = [i.select_the_formula for i in formula_display][0]
        except:
            formula_display = None


        if request.method == 'POST':
            try:
                class_form = ClassListForm(request.POST or None)

                # Class form
                class_form.is_valid()
                if list(class_form.cleaned_data.keys())[0] in list(request.POST.keys()):
                    try:
                        darasa = list(class_form.cleaned_data.values())[0]
                    except:
                        darasa = None

                    # Also saving the subjects
                    try:
                        my_subject1 = TeacherSetup.objects.filter(nm_id=req_pk, id=request.user.id)
                        my_subject = [i.my_subject for i in my_subject1][0]
                    except:
                        my_subject = None

                    # Registering
                    reg2 = TeacherSetup(nm_id=req_pk, id=request.user.id, my_class=darasa, my_subject=my_subject)
                    reg2.save()
            except:
                pass


            # Marks form
            marks_form = MarksForm(request.POST or None)
            try:
                '''
                Saving a form which has the following fields
                marks, paper1, paper2, paper3, subject, class, details of teacher
                '''
                # Type of the product
                product_type = SchoolProfile.objects.filter(pk=req_pk)
                product_type = [i.school_category for i in product_type][0]

                # for subject... the above one dont work
                try:
                    my_subject1 = TeacherSetup.objects.filter(nm_id=req_pk, id=request.user.id)
                    my_subject = [i.my_subject for i in my_subject1][0]
                except:
                    my_subject = None

                # for class
                try:
                    my_class1 = TeacherSetup.objects.filter(id=request.user.id, nm_id=req_pk)
                    my_class = [i.my_class for i in my_class1][0]
                except:
                    my_class = None

                # Name of teacher
                name_of_teacher = request.user
                '''
                Only saving the marks column, for the subjects with prac
                calculating the effective marks before sanding them,teacher 
                can change them within a certain period of time
                '''
                marks = None

                if product_type == 'p':
                    marks = dict(request.POST)['marks']
                    marks = formula_1(p1=marks, p2=None, p3=None)
                elif product_type == 'k':
                    marks = dict(request.POST)['marks']
                    marks = formula_1(p1=marks, p2=None, p3=None)
                elif product_type == 'a':
                    paper_1 = dict(request.POST)['paper_1']
                    try:
                        paper_2 = dict(request.POST)['paper_2']
                    except:
                        paper_2 = None
                    try:
                        paper_3 = dict(request.POST)['paper_3']
                    except:
                        paper_3 = None
                    #Also
                    if [''] * len(paper_1) == paper_2:
                        paper_2 = None
                    if [''] * len(paper_1) == paper_3:
                        paper_3 = None
                    #calculating marks column using p1, p2, p3
                    if formula_display == 'formula_2':
                        marks = formula_2(p1=paper_1, p2=paper_2, p3=paper_3)
                    elif formula_display == 'formula_3':
                        marks = formula_3(p1=paper_1, p2=paper_2, p3=paper_3)
                    else:
                        #default formula for advance even for students who dont have
                        #the p2 and p3
                        marks = formula_1(p1=paper_1, p2=paper_2, p3=paper_3)

                elif product_type == 'o':
                    paper_1 = dict(request.POST)['paper_1']
                    paper_2 = dict(request.POST)['paper_2']
                    if [''] * len(paper_1) == paper_2:
                        paper_2 = None

                    paper_3 = None
                    #calculating marks formula using p1 and p2
                    if formula_display == 'formula_2':
                        marks = formula_2(p1=paper_1, p2=paper_2, p3=paper_3)
                    elif formula_display == 'formula_3':
                        marks = formula_3(p1=paper_1, p2=paper_2, p3=paper_3)
                    else:
                        # default formula for olevel even for students who dont have
                        # the p2
                        marks = formula_1(p1=paper_1, p2=paper_2, p3=paper_3)



                marks_form.is_valid()
                # Form for all classes consists of marks
                #subject class and details of teacher
                dat = MarksData(
                    nm_id=req_pk, id=request.user.id,
                    marks=marks,
                    paper_1='',
                    paper_2='',
                    paper_3='',
                    class_of_the_subject=my_class,
                    name_of_the_submited_subject=str(my_subject),
                    name_of_subject_teacher=str(name_of_teacher),
                    submitted_time=str(time.strftime('%d-%m-%Y')))

                dat.save()
                txt2 = 'You have successfully submited your marks to academic'
                return redirect('/teacher/roles/')
            except:
                pass

    # ==================== ALL & SECRETARY ==============================================#
    try:
        # Name of the school
        nschool = SchoolProfile.objects.all().filter(nm_id=req_pk)

        # Type of the product
        product_type = SchoolProfile.objects.filter(pk=req_pk)
        product_type = [i.school_category for i in product_type][0]

        # List of students in the database created by academic teacher
        data_list = get_table_data(Students.objects.filter(nm_id=req_pk))


    except:
        pass
    try:
        # Authorization
        authorize = Authorize.objects.filter(pk=req_pk)  # FOR SECRETARY
        authorize = [i.authorize_the_results_to_be_printed_by_the_secretary for i in authorize][0]
    except:
        authorize = False


    # Classes to be displayed in the tables of the students
    if product_type == 'p':
        darasa = ['standard '+str(i) for i in range(1, 8)]
    elif product_type == 'o':
        darasa = ['form '+str(i) for i in range(1, 5)]
    elif product_type == 'a':
        darasa = ['form '+str(i) for i in range(5, 7)]
    elif product_type == 'k':
        darasa = ['level '+str(i) for i in range(1, 4)]
    else:
        darasa = None

    # defining the list
    req_list = None
    try:
        req_list = SubjectList.objects.filter(nm_id=req_pk)
        req_list = [i.name_of_the_subject for i in req_list]
    except:
        pass

    # Details of teacher status == FOR TEACHER ROLES
    subject_name = None
    class_name = None
    try:
        details = TeacherSetup.objects.filter(nm_id=req_pk, id=request.user.id)
        subject_name = [i.my_subject for i in details][0]
        class_name = [i.my_class for i in details][0]
    except:
        pass

    image = image_show(request=request, req_pk=req_pk)
    nameschool = name_school_show(request=request, req_pk=req_pk)

    dt = {
        # For adding students
        'first_form': first_form,
        # For list of classes
        'class_form': class_form,
        # List of the student in the database
        # used by academic only
        'data_list1': data_list,
        # Name of the school
        'nschool': nschool,
        'name_school': nameschool,
        'image': image,
        # Role of the teacher from the administrator
        'req_role': encode(req_role),
        # For product type
        'product_type': product_type,
        'txt1': txt1,
        #for classes
        'darasa': darasa,
        # authorization
        'authorize': authorize,
        # for teacher
        'tea_form': tea_form,
        # list of the subject
        'req_list': req_list,
        # details of teacher roles
        'subject_name': subject_name,
        'class_name': class_name,
        # for filling marks
        'marks_form': marks_form,
        # submited_marks
        'submited_marks': submited_marks,
        # formula to display
        'formula_display': formula_display,
        #text for submited form
        'txt2': txt2,
        'files_upload': files_upload,


    }
    return render(request, 'teacher_roles.html', dt)

@authenticated_te
def teacher_work(request, *args, **kwargs):
    req_role = None
    req_pk = None
    try:
        # his own key
        data_key = RequiredKey.objects.filter(id=request.user.id)
        # using admin pk
        req_role, req_pk = required_key([i.user_key for i in data_key][0])
    except:
        pass

    type_btn = AcademicBtnForm(request.POST or None)
    if request.method == 'POST':
        type_btn.is_valid()

        if type_btn.clean():
            d = type_btn.cleaned_data['type_of_table_to_be_filled_by_teacher']
            reg = AcademicBtn(type_of_table_to_be_filled_by_teacher=d, nm_id=req_pk, id=request.user.id)
            reg.save()
            redirect("/teacher/work/")


    enabled = None
    try:
        enabled = AcademicBtn.objects.filter(nm_id=req_pk, id=request.user.id)
        enabled = [i.type_of_table_to_be_filled_by_teacher for i in enabled][0]
    except:
        pass
    image = image_show(request=request, req_pk=req_pk)
    nschool = name_school_show(request=request, req_pk=req_pk)
    dt = {

        'req_role': encode(req_role),
        'type_btn': type_btn,
        'enabled': enabled,
        'image': image,
        'nschool': nschool,
    }
    return render(request, 'teacher_work.html', dt)

@authenticated_te
def teacher_roles_academic_subject(request, *args, **kwargs):

    # Loading the key from the database first
    data_key = RequiredKey.objects.filter(id=request.user.id)
    # using admin pk
    req_role, req_pk = required_key([i.user_key for i in data_key][0])  ################################

    subject_list_form = SubjectListForm(request.POST or None)
    subject_list_form.is_valid()
    if request.method == 'POST':
        subject_list_form.is_valid()
        if subject_list_form.clean():
            sub = subject_list_form.cleaned_data['name_of_the_subject']
            reg = SubjectList(nm_id=req_pk, name_of_the_subject=sub)
            reg.save()



    # defining the list
    req_list = None
    try:
        req_list = SubjectList.objects.filter(nm_id=req_pk)
        req_list = [i.name_of_the_subject for i in req_list]
    except:
        pass
    image = image_show(request=request, req_pk=req_pk)
    nschool = name_school_show(request=request, req_pk=req_pk)

    dt = {
        'form': subject_list_form,
        'req_list': req_list,
        'image': image,
        'nschool': nschool,
    }
    return render(request, 'teacher_roles_academic_subject.html', dt)

@authenticated_te
def teacher_roles_academic_subject_delete(request, value, *args, **kwargs):
    # his own key so as to get the admin pk -- nm
    data_key = RequiredKey.objects.filter(id=request.user.id)
    # using admin pk
    req_role, req_pk = required_key([i.user_key for i in data_key][0])
    sub = SubjectList.objects.filter(nm_id=req_pk, name_of_the_subject=str(value))
    #sub.delete()
    if request.method == 'POST':
        sub.delete()
        return redirect('/teacher/roles/academic/subject/')

    try:
        sub = [i.name_of_the_subject for i in sub][0]
    except:
        sub = None
    image = image_show(request=request, req_pk=req_pk)
    nschool = name_school_show(request=request, req_pk=req_pk)
    dt = {
        'sub':sub,
        'image': image,
        'nschool': nschool,
    }
    return render(request, 'teacher_roles_academic_subject_delete.html', dt)

@authenticated_te
def teacher_roles_academic_students_delete(request, first_name, middle_name, last_name, sex, darasa, *args, **kwargs):
    # his own key so as to get the admin pk -- nm
    data_key = RequiredKey.objects.filter(id=request.user.id)
    # using admin pk
    req_role, req_pk = required_key([i.user_key for i in data_key][0])
    sub = Students.objects.filter(
        nm_id=req_pk, first_name__iexact=first_name,
        middle_name=middle_name, last_name__iexact=last_name, sex__iexact=sex, darasa__iexact=darasa)

    if request.method == 'POST':
        sub.delete()
        return redirect('/teacher/roles/')
    print([i.first_name + '\t' + i.last_name for i in sub])
    try:
        sub = [i.first_name + '\t' + i.middle_name + '\t' + i.last_name for i in sub][0]
    except:
        sub = None
    image = image_show(request=request, req_pk=req_pk)
    nschool = name_school_show(request=request, req_pk=req_pk)

    dt = {
        'sub': sub,
        'image': image,
        'nschool': nschool,
    }
    return render(request, 'teacher_roles_academic_students_delete.html', dt)

@authenticated_te
def teacher_work_academic_general_setup(request, *args, **kwargs):
    # his own key so as to get the admin pk -- nm
    data_key = RequiredKey.objects.filter(id=request.user.id)
    # using admin pk
    req_role, req_pk = required_key([i.user_key for i in data_key][0])

    try:
        product_type = SchoolProfile.objects.filter(nm_id=req_pk)
        product_type = [i.school_category for i in product_type][0]
    except:
        product_type = None

    form = AcademicSetupForm(request.POST or None)
    if request.method == 'POST':
        form.is_valid()
        name_of_the_examination = form.cleaned_data['name_of_the_examination']
        a = form.cleaned_data['A']
        b = form.cleaned_data['B']
        c = form.cleaned_data['C']
        d = form.cleaned_data['D']
        if product_type == 'a':
            e = form.cleaned_data['E']
            s = form.cleaned_data['S']
        else:
            e = None
            s = None
        f = form.cleaned_data['F']

        division_1 = form.cleaned_data['division_1']
        division_2 = form.cleaned_data['division_2']
        division_3 = form.cleaned_data['division_3']
        division_4 = form.cleaned_data['division_4']
        division_0 = form.cleaned_data['division_0']

        reg = AcademicSetup(
            name_of_the_examination=name_of_the_examination,
            A=a, B=b, C=c, D=d, E=e, F=f, S=s,
            division_1=division_1, division_2=division_2,
            division_3=division_3, division_4=division_4,
            division_0=division_0,
            nm_id=req_pk, id=request.user.id
        )
        reg.save()

    image = image_show(request=request, req_pk=req_pk)
    nschool = name_school_show(request=request, req_pk=req_pk)
    try:
        pro = AcademicSetup.objects.filter(nm_id=req_pk, id=request.user.id)
        data_list = [[i.name_of_the_examination, i.A, i.B, i.C, i.D, i.E, i.S, i.F, i.division_1,
                      i.division_2, i.division_3, i.division_4, i.division_0,
                      ] for i in pro]
    except:
        data_list = None


    print(product_type, data_list)
    dt = {
        'form': form,
        'image': image,
        'nschool': nschool,
        'product_type': product_type,
        'data_list': data_list,
    }
    return render(request, 'teacher_work_academic_general_setup.html', dt)

@authenticated_te
def teacher_work_academic_generate_table(request, *args, **kwargs):
    # his own key so as to get the admin pk -- nm
    data_key = RequiredKey.objects.filter(id=request.user.id)
    # using admin pk
    req_role, req_pk = required_key([i.user_key for i in data_key][0])
    try:
        # Type of the product
        product_type = SchoolProfile.objects.filter(pk=req_pk)
        product_type = [i.school_category for i in product_type][0]
    except:
        product_type = None


    try:
        data_form = MarksData.objects.filter(nm_id=req_pk)
        required_form = [[i.name_of_subject_teacher, i.class_of_the_subject,
                         i.name_of_the_submited_subject, i.submitted_time]
                         for i in data_form]
    except:
        required_form = []

    if required_form == []:
        required_index = 0
    else:
        required_index = 1


    #################################################################################

    # form with marks of all students
    internal_form = []
    try:
        data_form = MarksData.objects.filter(nm_id=req_pk)
        internal_form = [[i.class_of_the_subject, i.name_of_the_submited_subject,
                         i.marks] for i in data_form]
    except:
        pass
    total_list = []
    required_list0 = []
    # Expected output  {form n:[[sub list], [data list]]
    for j in internal_form:
        try:
            total_list.append([j[0], j[1], j[2]])
        except:
            pass


    if product_type == 'o':
        for m in ['form '+str(i) for i in range(1, 5)]:
            try:
                dt0 = [i for i in total_list if i[0] == m]
                sub_list = [j[1] for j in dt0]
                data_labels = ['Name', 'Sex'] + list(sub_list)
                marks = [array_generator(j[2]) for j in dt0]
                marks = concatenate([i.reshape(-1, 1) for i in array(marks)], axis=1)

                name_list = [[i.first_name, i.middle_name, i.last_name,
                              i.sex, i.darasa]
                             for i in Students.objects.filter(nm_id=req_pk)]
                n = [i for i in name_list if i[-1] == m]
                name_list = [[i[0] + ' ' + i[1] + ' ' + i[2]] for i in n]
                sex_list = [i[3] for i in n]
                data_content = np.concatenate(
                    [i for i in
                       [
                           np.array(name_list).reshape(-1, 1),
                           np.array(sex_list).reshape(-1, 1),
                           np.array(marks).reshape(-len(marks[0]), len(marks)),
                       ]], axis=1)
                required_list0.append([m, [data_labels, data_content]])
            except:
                pass


    if product_type == 'p':
        for m in ['standard '+str(i) for i in range(1, 8)]:
            try:
                dt0 = [i for i in total_list if i[0] == m]
                sub_list = [j[1] for j in dt0]
                data_labels = ['Name', 'Sex'] + list(sub_list)
                marks = [array_generator(j[2]) for j in dt0]
                marks = concatenate([i.reshape(-1, 1) for i in array(marks)], axis=1)

                name_list = [[i.first_name, i.middle_name, i.last_name,
                              i.sex, i.darasa]
                             for i in Students.objects.filter(nm_id=req_pk)]
                n = [i for i in name_list if i[-1] == m]
                name_list = [[i[0] + ' ' + i[1] + ' ' + i[2]] for i in n]
                sex_list = [i[3] for i in n]
                data_content = np.concatenate(
                    [i for i in
                       [
                           np.array(name_list).reshape(-1, 1),
                           np.array(sex_list).reshape(-1, 1),
                           marks,
                       ]], axis=1)

                required_list0.append([m, [data_labels, data_content]])
            except:
                pass
            #break

    if product_type == 'k':
        for m in ['level '+str(i) for i in range(1, 4)]:
            try:
                dt0 = [i for i in total_list if i[0] == m]
                sub_list = [j[1] for j in dt0]
                data_labels = ['Name', 'Sex'] + list(sub_list)
                marks = [array_generator(j[2]) for j in dt0]
                marks = concatenate([i.reshape(-1, 1) for i in array(marks)], axis=1)

                name_list = [[i.first_name, i.middle_name, i.last_name,
                              i.sex, i.darasa]
                             for i in Students.objects.filter(nm_id=req_pk)]
                n = [i for i in name_list if i[-1] == m]
                name_list = [[i[0] + ' ' + i[1] + ' ' + i[2]] for i in n]
                sex_list = [i[3] for i in n]
                data_content = np.concatenate(
                    [i for i in
                       [
                           np.array(name_list).reshape(-1, 1),
                           np.array(sex_list).reshape(-1, 1),
                           marks,
                       ]], axis=1)
                required_list0.append([m, [data_labels, data_content]])
            except:
                pass
            #break

    if product_type == 'a':
        for m in ['form '+str(i) for i in range(5, 7)]:
            try:
                dt0 = [i for i in total_list if i[0] == m]
                sub_list = [j[1] for j in dt0]
                data_labels = ['Name', 'Sex'] + list(sub_list)
                marks = [array_generator(j[2]) for j in dt0]
                marks = concatenate([i.reshape(-1, 1) for i in array(marks)], axis=1)

                gs = re.compile(r'(^gs|^general[\s]*stud[a-z\s]*|111)$')
                gs_ind = [sub_list.index(i) for i in sub_list if gs.match(i) is not None][0]
                #print(gs_ind, marks[3])
                name_list = [[i.first_name, i.middle_name, i.last_name,
                              i.sex, i.darasa]
                             for i in Students.objects.filter(nm_id=req_pk)]
                n = [i for i in name_list if i[-1] == m]
                name_list = [[i[0] + ' ' + i[1] + ' ' + i[2]] for i in n]
                sex_list = [i[3] for i in n]
                data_content = np.concatenate(
                    [i for i in
                       [
                           np.array(name_list).reshape(-1, 1),
                           np.array(sex_list).reshape(-1, 1),
                           marks,
                       ]], axis=1)
                required_list0.append([m, [data_labels, data_content]])
            except:
                pass
            #break

    # for class form
    class_form = ClassListForm(request.POST or None)

    darasa = None
    if request.method == 'POST':
        class_form.is_valid()
        try:
            darasa = list(class_form.cleaned_data.values())[0]
            inter_val = IntermediateValue(nm_id=req_pk, id=request.user.id, inter_val=darasa)
            inter_val.save()
        except:
            darasa = None

    try:
        required_list = dict(required_list0)[darasa]
    except:
        required_list = None

    try:
        data_labels = required_list[0]
        data_content = required_list[1]
    except:
        data_labels = None
        data_content = None


    #print((data_content[:, 2:]))
    try:
        grade_data0 = grade_func(request=request, req_pk=req_pk, list_of_marks=data_content[:, 2:],
                name=data_content[:, 0], sex=data_content[:, 1],
                list_of_subject=data_labels[2:], darasa=product_type,
                class_of_the_student=darasa)

        grade_label = grade_data0.encode()[1]
        grade_data = grade_data0.encode()[0]
    except:
        grade_label = None
        grade_data = None
        grade_data0 = 0


    image = image_show(request=request, req_pk=req_pk)
    nschool = name_school_show(request=request, req_pk=req_pk)

    try: ind=len(grade_data)
    except: ind = None

    #for second form
    upload_form = UploadToAdminForm()
    if request.method == 'POST':
        upload_form =UploadToAdminForm(request.POST, request.FILES)
        upload_form.is_valid()
        if 'internal_files' in list(request.POST.keys()):
            intval = IntermediateValue.objects.filter(nm_id=req_pk, id=request.user.id)
            intval = [i.inter_val for i in intval][0]
            required_list = dict(required_list0)[intval]
            data_labels = required_list[0]
            data_content = required_list[1]
            grade_data0 = grade_func(request=request, req_pk=req_pk, list_of_marks=data_content[:, 2:],
                                     name=data_content[:, 0], sex=data_content[:, 1],
                                     list_of_subject=data_labels[2:], darasa=product_type,
                                     class_of_the_student=intval)

            for i in grade_data0.files():
                reg = UploadToAdmin(internal_files=i, nm_id=req_pk)
                reg.save()
                reg = None
            #deleting the database to prevent backflow
            final_data = MarksData.objects.filter(
                nm_id=req_pk, class_of_the_subject=intval)
            final_data.delete()



            return redirect('/teacher/work/academic/generate/table/')




    dt = {
        'required_form': required_form,
        'required_index': required_index,
        'product_type': product_type,
        'class_form': class_form,
        'image': image,
        'nschool': nschool,
        'data_labels': data_labels,
        'data_content': data_content,
        'darasa': darasa,
        'grade_data': grade_data,
        'grade_label': grade_label,
        'ind': ind,
        'upload_form': upload_form,


    }
    return render(request, 'teacher_work_academic_generate_table.html', dt)

@authenticated_te
def teacher_roles_teacher_confirm(request, value, *args, **kwargs):
    # his own key so as to get the admin pk -- nm
    data_key = RequiredKey.objects.filter(id=request.user.id)
    # using admin pk
    req_role, req_pk = required_key([i.user_key for i in data_key][0])
    subject = SubjectList.objects.filter(nm_id=req_pk, name_of_the_subject=str(value))
    #sub.delete()
    if request.method == 'POST':# for subjects

        try:
            subject = [i.name_of_the_subject for i in subject][0]
        except:
            subject = None

        try:
            my_class1 = TeacherSetup.objects.filter(id=request.user.id, nm_id=req_pk)
            my_class = [i.my_class for i in my_class1][0]
        except:
            my_class = None

        reg = TeacherSetup(nm_id=req_pk, id=request.user.id, my_class=my_class, my_subject=subject)
        reg.save()
        return redirect('/teacher/roles/')

    try:
        subject = [i.name_of_the_subject for i in subject][0]
    except:
        subject = None
    image = image_show(request=request, req_pk=req_pk)
    nschool = name_school_show(request=request, req_pk=req_pk)
    dt = {
    'sub': subject,
    'image': image,
    'nschool': nschool,
    }
    return render(request, 'teacher_roles_teacher_confirm.html', dt)

@authenticated_te
def teacher_roles_formula(request, *args, **kwargs):
    # his own key so as to get the admin pk -- nm
    data_key = RequiredKey.objects.filter(id=request.user.id)
    # using admin pk
    req_role, req_pk = required_key([i.user_key for i in data_key][0])
    prac_form = PracticalFormulaForm(request.POST or None)

    if request.method == 'POST':
        prac_form.is_valid()
        dat = prac_form.cleaned_data['select_the_formula']

        #Because he is the teacher
        reg = PracticalFormula(nm_id=req_pk, id=request.user.id,
                               select_the_formula=dat)
        reg.save()
        return redirect('/teacher/roles/')
    image = image_show(request=request, req_pk=req_pk)
    nschool = name_school_show(request=request, req_pk=req_pk)
    dt = {
        'prac_form': prac_form,
        'image': image,
        'nschool': nschool,
    }
    return render(request, 'teacher_roles_formula.html', dt)

