from django.contrib import admin
from .models import SchoolProfile, MyUser, Post, AcademicBtn, \
    MarksData, SecretaryRoles, Profile, UploadToAdmin, IntermediateValue
from .models import ClassList, Students, SubjectList, AcademicSetup, Authorize, TeacherSetup, PracticalFormula
# Register your models here.

admin.site.register(UploadToAdmin)
admin.site.register(Profile)
admin.site.register(SchoolProfile)
admin.site.register(MyUser)
admin.site.register(Post)
admin.site.register(Authorize)
admin.site.register(SecretaryRoles)
admin.site.register(AcademicSetup)
admin.site.register(AcademicBtn)
admin.site.register(SubjectList)
admin.site.register(ClassList)
admin.site.register(Students)
admin.site.register(MarksData)
admin.site.register(PracticalFormula)
admin.site.register(TeacherSetup)
admin.site.register(IntermediateValue)

