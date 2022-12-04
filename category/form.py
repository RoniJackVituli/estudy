from django import forms
from category.models import Course, HomeWork, CommentHomeWork


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("department", "year", "semester", "kind_of")


class HomeWorkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        fields = ("nameFile", "file", "course")


class CreatCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("department", "year", "semester", "name_course", "kind_of")
        widgets = {
            "name_course": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "bg-light form-control",
                }
            ),
        }


class CommentHomeWorkForm(forms.ModelForm):
    class Meta:
        model = CommentHomeWork
        fields = ("message",)
        widgets = {
            "message": forms.Textarea(
                attrs={
                    "class": "form-control ml-1 shadow-none textarea",
                    "style": "height: 90px;",
                }
            )
        }
