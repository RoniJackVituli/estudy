import email

from accounts.models import Student, Lecturer, User
from django import forms


class StudentForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"type": "text", "class": "bg-light form-control"})
    )

    class Meta:
        model = Student
        fields = (
            "first_name",
            "last_name",
            "Phone",
            "ID",
            "department",
            "year",
            "semester",
        )
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "bg-light form-control",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "bg-light form-control",
                }
            ),
            "Phone": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "bg-light form-control",
                }
            ),
            "ID": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "bg-light form-control",
                }
            ),
        }

    def clean_ID(self):
        ID = self.cleaned_data.get("ID")
        if not ID.isdecimal():
            raise forms.ValidationError("ID must to contain only digits.")
        elif len(ID) != 9:
            raise forms.ValidationError("ID must to contain 9 digits.")
        elif (
            Student.objects.filter(ID=ID).exists()
            and len(Student.objects.filter(ID=ID)) > 1
        ) or (Lecturer.objects.filter(ID=ID).exists()):
            raise forms.ValidationError("ID exsits")
        return ID


class UserUpdate(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("email", "imag_profile")
        widgets = {
            "email": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "bg-light form-control",
                }
            ),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Confirm password does not match")
        return password


class LecturerForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"type": "text", "class": "bg-light form-control"})
    )

    class Meta:
        model = Student
        fields = ("first_name", "last_name", "Phone", "ID")
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "bg-light form-control",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "bg-light form-control",
                }
            ),
            "Phone": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "bg-light form-control",
                }
            ),
            "ID": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "bg-light form-control",
                }
            ),
        }

    def clean_ID(self):
        ID = self.cleaned_data.get("ID")
        if not ID.isdecimal():
            raise forms.ValidationError("ID must to contain only digits.")
        elif len(ID) != 9:
            raise forms.ValidationError("ID must to contain 9 digits.")
        elif (Student.objects.filter(ID=ID).exists()) or (
            Lecturer.objects.filter(ID=ID).exists()
            and len(Lecturer.objects.filter(ID=ID)) > 1
        ):
            raise forms.ValidationError("ID exsits")
        return ID
