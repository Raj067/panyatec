from django import forms
from .models import *
#NOTE: SECRETARY FORM SHOULD BE DELETED ........... NOT USED

class UploadToAdminForm(forms.ModelForm):
    class Meta:
        model = UploadToAdmin
        fields = '__all__'


class AcademicSetupForm(forms.ModelForm):
    class Meta:
        model = AcademicSetup
        fields = '__all__'

class AuthorizeForm(forms.ModelForm):
    class Meta:
        model = Authorize
        fields = '__all__'

class SecretaryRolesForm(forms.ModelForm):
    class Meta:
        model = SecretaryRoles
        fields = '__all__'

class PracticalFormulaForm(forms.ModelForm):
    ch = [
        ('formula_1', 'formula 1'),
        ('formula_2', 'formula 2'),
        ('formula_3', 'formula 3'),
    ]
    select_the_formula = forms.ChoiceField(choices=ch, widget=forms.RadioSelect, initial='formula_1')
    class Meta:
        model = PracticalFormula
        fields = '__all__'

class AcademicBtnForm(forms.ModelForm):
    ch = [
        ('name', 'name of the students'),
        ('number', 'number of the students'),
        ('none', 'Not authorize to access table'),
    ]
    type_of_table_to_be_filled_by_teacher = \
        forms.ChoiceField(choices=ch, widget=forms.RadioSelect, initial='name')

    class Meta:
        model = AcademicBtn
        fields = '__all__'

class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        exclude = ['nm']

class SchoolProfileForm(forms.ModelForm):
    class Meta:
        model = SchoolProfile
        fields = '__all__'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        exclude = ['nm']


class ClassListForm(forms.ModelForm):
    class Meta:
        model = ClassList
        fields = '__all__'

class SubjectListForm(forms.ModelForm):
    class Meta:
        model = SubjectList
        fields = '__all__'


class MarksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MarksForm, self).__init__(*args, **kwargs)
        #self.fields['paper_1'].widget.attrs['cols'] = 1
        self.fields['paper_1'].widget.attrs['size'] = 1
        self.fields['paper_2'].widget.attrs['size'] = 1
        self.fields['paper_3'].widget.attrs['size'] = 1
        self.fields['marks'].widget.attrs['size'] = 1

    class Meta:
        model = MarksData
        fields = '__all__'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
