from django import forms
from HomePage.models import Post
from accounts.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "description")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control border-0"}),
            "description": forms.Textarea(
                attrs={
                    "name": "message",
                    "id": "msgus",
                    "cols": "10",
                    "rows": "5",
                    "class": "form-control bg-light",
                }
            ),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("permissions",)
