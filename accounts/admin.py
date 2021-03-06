from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Selection

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['name_of_the_school',
                  'role',
                    'username', 'email', 'phone_number']

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Selection)