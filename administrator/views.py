from django.shortcuts import render, redirect
from algorithims.decoretor import *
import datetime
import numpy as np
from .forms import *
from .models import *
from algorithims.front import *


@authenticated_ad
def administrator_user(request, *args, **kwargs):
    nschool = None
    image = None
    try:
        school = SchoolProfile.objects.filter(nm_id=request.user.id)
        nschool = [i.name_of_the_school for i in school][0]
        image = [i.logo_of_the_school for i in school][0].url
    except:
        pass
    # Information of teacher
    try:
        info = Profile.objects.filter(nm_id=request.user.id)
        my_name = [[str(i.first_name) + ' ' + str(i.middle_name) + ' ' +
                    str(i.last_name)]
                   for i in info]
        phone_number = [i.phone_number for i in info]
        my_email = [i.my_email_address for i in info]
        my_image = [i.upload_image.url for i in info]
        my_bio = [i.bio for i in info]
        linkedin = [i.your_linkedin_profile for i in info]

        facebook = [i.your_facebook_profile for i in info]
        twitter = [i.your_twitter_profile for i in info]
        instagram = [i.your_instagram_profile for i in info]

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

    txt1 = 0
    txt2 = 0
    txt3 = 0
    form = MyUserForm(request.POST or None)
    if form.is_valid():
        txt1 = 'You have successfully add new user'
        txt2 = 'You have successfully delete user'
        fname = form.cleaned_data['first_name']
        sname = form.cleaned_data['second_name']
        #vkey = form.cleaned_data['value_key']
        role = form.cleaned_data['role']

        val = generate_key(role=role, val=request.user.id)
        reg = MyUser(nm_id=request.user.id, first_name=fname, second_name=sname, role=role, value_key=val)
        #Only saving the important data
        txt3 = str(val)
        reg.save()

    data_list = MyUser.objects.filter(nm_id=request.user.id)
    try:
        my_key = [i.value_key for i in data_list]
    except:
        my_key = None
    print(my_key)

    try:
        data = zip(my_image, my_name, phone_number, my_email, my_bio,
                   linkedin, facebook, twitter, instagram, my_key)

    except:
        data = None
    dt = {
        'form': form,
        'txt1': txt1,
        'txt2': txt2,
        'txt3': txt3,
        'data_list': data_list,
        'nschool': nschool,
        'image': image,
        'my_key1': my_key,
        'data': data,
    }
    return render(request, 'administrator_users.html', dt)

@authenticated_ad
def administrator_files(request, *args, **kwargs):
    nschool = None
    image = None
    try:
        school = SchoolProfile.objects.filter(nm_id=request.user.id)
        nschool = [i.name_of_the_school for i in school][0]
        image = [i.logo_of_the_school for i in school][0].url
    except:
        pass
    required_form = []
    try:
        data_form = MarksData.objects.filter(nm_id=request.user.id)
        required_form = [[i.name_of_subject_teacher, i.class_of_the_subject,
                          i.name_of_the_submited_subject, i.submitted_time] for i in data_form]
    except:
        pass
    if required_form == []:
        required_index = 0
    else:
        required_index = 1
    dt = {
        'required_form': required_form,
        'required_index': required_index,
        'nschool': nschool,
        'image': image,
    }
    return render(request, 'administrator_files.html', dt)

@authenticated_ad
def administrator_home(request, *args, **kwargs):
    form10 = PostForm(request.POST or None)
    txt = 0
    form10.is_valid()
    if request.method == 'POST':
        if form10.clean():
            msg = form10.cleaned_data['send_notifications_to_teachers']
            #deleting the previous notification
            reg = Post(sender = request.user,
                       send_notifications_to_teachers=msg,
                       nm_id=request.user.id)
            txt = 'Your post have been sent successfully'
            reg.save()

    subjects = None
    try:
        subjects = [i.name_of_the_subject for i in SubjectList.objects.filter(nm_id=request.user.id)]
    except:
        pass

    product_type = None

    try:
        product_type = SchoolProfile.objects.filter(nm_id=request.user.id)
        product_type = [i.school_category for i in product_type][0]
    except:
        pass
    print(request.user.role)
    # Classes to be displayed in the home page
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

    # List of students in the database created by academic teacher
    data_list = None
    try:
        data_list = Students.objects.filter(nm_id=request.user.id)
        data_list = [[i.first_name, i.middle_name, i.last_name,
                      i.candidate_number, i.sex, i.darasa] for i in data_list]
    except:
        pass

    nschool = None
    image = None
    try:
        school = SchoolProfile.objects.filter(nm_id=request.user.id)
        nschool = [i.name_of_the_school for i in school][0]
        image = [i.logo_of_the_school for i in school][0].url
    except:
        pass

    dt = {
        'form10': form10,
        'txt': txt,
        'username': request.user,
        'subjects': subjects,
        'darasa': darasa,
        'data_list': data_list,
        'product_type': product_type,
        'nschool': nschool,
        'image':image,
    }
    return render(request, 'administrator_home.html', dt)

@authenticated_ad
def administrator_payment(request, *args, **kwargs):
    tm = datetime.datetime.now()
    nschool = None
    image = None
    try:
        school = SchoolProfile.objects.filter(nm_id=request.user.id)
        nschool = [i.name_of_the_school for i in school][0]
        image = [i.logo_of_the_school for i in school][0].url
    except:
        pass
    dt = {
        'time': tm,
        'nschool': nschool,
        'image': image,
    }
    return render(request, 'administrator_payment.html', dt)

@authenticated_ad
def administrator_profile(request, *args, **kwargs):
    txt = 0
    obj = None
    req_obj = []

    form1 = SchoolProfileForm()
    if request.method == 'POST':
        form1 = SchoolProfileForm(request.POST, request.FILES)
        form1.is_valid()
        if form1.clean():
            #print('rajabu')
            #for replacing the old data
            nschool = form1.cleaned_data['name_of_the_school']
            ashcool = form1.cleaned_data['address_of_the_school']
            eschool = form1.cleaned_data['email_of_the_school']
            wschool = form1.cleaned_data['website_of_the_school']
            mschool = form1.cleaned_data['motto_of_the_school']
            vschool = form1.cleaned_data['vision_of_the_school']
            lschool = form1.cleaned_data['logo_of_the_school']
            dschool = form1.cleaned_data['description_of_the_school']
            cschool = form1.cleaned_data['school_category']
            print(form1.cleaned_data)
            reg = SchoolProfile(nm_id=request.user.id, id=request.user.id,
                            name_of_the_school=nschool,
                            address_of_the_school=ashcool,
                            email_of_the_school=eschool,
                            website_of_the_school=wschool,
                            logo_of_the_school=lschool,
                            vision_of_the_school=vschool,
                            motto_of_the_school=mschool,
                            description_of_the_school=dschool,
                            school_category=cschool)
        txt = 'You have successfully updated your ' \
              'profile. refresh your browser to apply changes'
        reg.save()

    try:
        obj = SchoolProfile.objects.filter(nm_id=request.user.id)

        req_obj = [[i.name_of_the_school, i.address_of_the_school,
                    i.email_of_the_school, i.website_of_the_school,
                    i.vision_of_the_school, i.motto_of_the_school,
                    i.description_of_the_school, i.logo_of_the_school]
                   for i in obj]
        req_obj = np.array(req_obj).reshape(8)

    except:
        pass

    dt = {
        'form1': form1,
        'obj': obj,
        'req_obj': req_obj,
        'txt': txt,
    }
    return render(request, 'administrator_profile.html', dt)

@authenticated_ad
def administrator_results(request, *args, **kwargs):
    nschool = None
    image = None
    try:
        school = SchoolProfile.objects.filter(nm_id=request.user.id)
        nschool = [i.name_of_the_school for i in school][0]
        image = [i.logo_of_the_school for i in school][0].url
    except:
        pass
    form = AuthorizeForm(request.POST or None)
    if request.method == 'POST':
        form.is_valid()
        d = form.cleaned_data['authorize_the_results_to_be_printed_by_the_secretary']
        reg = Authorize(nm_id=request.user.id, id=request.user.id,
                        authorize_the_results_to_be_printed_by_the_secretary=d)
        reg.save()
        print(d)
    authorized = False
    try:
        authorized = Authorize.objects.filter(nm_id=request.user.id)
        authorized = [i.authorize_the_results_to_be_printed_by_the_secretary for i in authorized][0]
    except:
        pass
    dt = {
        'form': form,
        'authorized': authorized,
        'nschool': nschool,
        'image': image,
    }
    return render(request, 'administrator_results.html', dt)

@authenticated_ad
def notifications(request, *args, **kwargs):
    form10 = PostForm(request.POST or None)
    txt = 0
    form10.is_valid()
    if request.method == 'POST':
        if form10.clean():
            msg = form10.cleaned_data['send_notifications_to_teachers']
            #deleting the previous notification
            reg = Post(sender = request.user,
                       send_notifications_to_teachers=msg,
                       nm_id=request.user.id)
            txt = 'Your post have been sent successfully'
            reg.save()
    notifications = Post.objects.all().filter(nm_id=request.user.id)
    try:  # for notifications
        sender = [i.sender for i in notifications]
        tm = [i.time_sent for i in notifications]
        notifications = [i.send_notifications_to_teachers for i in notifications]
        if notifications == []:
            notifications = 'No notification now'
    except:
        notifications = None
        sender = None
        tm =None
    data = zip(sender, tm, notifications)
    p = [[i, j, k] for i, j, k in data][::-1]

    dt = {
        'form10': form10,
        'txt': txt,
        'my_data': p,


    }
    return render(request, 'notifications.html', dt)
