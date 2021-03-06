from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Selection
from allauth.account.forms import SignupForm
from allauth.account.forms import LoginForm


'''for admin form'''
#================================================================================
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('name_of_the_school',
                  'role',
                   'username', 'email_address', 'phone_number')



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('name_of_the_school',
                  'role',
                    'username', 'email_address', 'phone_number')
#================================================================================


class MyCustomLoginForm(LoginForm):
    #add new fields if needed for login purposes
    def login(self, *args, **kwargs):

        # Add your own processing here.
        user = super(MyCustomLoginForm, self).login(*args, **kwargs)

        user.login()
        # You must return the original result.
        return user



'''for administrator signup'''

class MyCustomSignupForm_ad(SignupForm):
    name_of_the_school = forms.CharField(max_length=30, label='Name of the school', required=True)
    email_address = forms.EmailField(required=True, label='Email')
    role = forms.CharField(initial='ad', max_length=2, required=False, disabled=True)
    phone_number = forms.CharField(max_length=10, min_length=10)
    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm_ad, self).save(request)

        # Add your own processing here.
        user.name_of_the_school = self.cleaned_data['name_of_the_school']
        user.email_address = self.cleaned_data['email_address']
        user.role = self.cleaned_data['role']
        user.phone_number = self.cleaned_data['phone_number']

        user.save()
        # You must return the original result.
        return user

'''For teacher signup'''
class MyCustomSignupForm_te(SignupForm):
    name_of_the_school = forms.CharField(initial='Teacher', disabled=True, max_length=8, required=False)
    email_address = forms.EmailField(required=True, label='Email')
    role = forms.CharField(initial='te', max_length=2, required=False, disabled=True)
    phone_number = forms.CharField(max_length=10, min_length=10)
    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm_te, self).save(request)

        # Add your own processing here.
        user.name_of_the_school = self.cleaned_data['name_of_the_school']
        user.email_address = self.cleaned_data['email_address']
        user.role = self.cleaned_data['role']
        user.phone_number = self.cleaned_data['phone_number']

        user.save()
        # You must return the original result.
        return user



#----------------------------------------------------------------------------------------------------------
from allauth.account.forms import ResetPasswordForm
class MyCustomResetPasswordForm(ResetPasswordForm):

    def save(self):

        # Ensure you call the parent class's save.
        # .save() returns a string containing the email address supplied
        email_address = super(MyCustomResetPasswordForm, self).save()

        # Add your own processing here.

        # Ensure you return the original result
        return email_address

#==========================================================================================================
class Select(forms.ModelForm):
    class Meta:
        model = Selection
        fields = '__all__'
