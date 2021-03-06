from django.shortcuts import render
from algorithims.decoretor import *
# Create your views here.

@unauthenticated_administrator
@unauthenticated_teacher
def main_home(request, *args, **kwargs):
    dt = {
    }
    return render(request, 'main_homepage.html', dt)


def help_page(request, *args, **kwargs):
    dt = {

    }
    return render(request, 'help.html', dt)
