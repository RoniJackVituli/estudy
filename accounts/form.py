from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Lecturer
from django.db import transaction
from django.contrib.auth import get_user_model

# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

User = get_user_model()


class StudentUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "zmdi zmdi-email",
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "class": "zmdi zmdi-email",
                }
            ),
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.save()
        return user


class LecturerUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "zmdi zmdi-email",
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "class": "zmdi zmdi-email",
                }
            ),
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_lecturer = True
        user.save()
        lecturer = Lecturer.objects.create(user=user)
        lecturer.save()
        return user


# class StudentProfileForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ('First_Name', 'Last_Name', 'ID_Number', 'Phone' , 'profileImag')


# class LecturerProfileForm(forms.ModelForm):
#     class Meta:
#         model = Lecturer
#         fields = ('First_Name', 'Last_Name', 'ID_Number', 'Phone' , 'profileImag')
