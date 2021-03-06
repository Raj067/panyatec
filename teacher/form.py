from django.forms import ModelForm

from .models import RequiredKey



class RequiredKeyForm(ModelForm):
    class Meta:
        model = RequiredKey
        fields = '__all__'
