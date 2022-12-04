from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login

from .form import StudentUserCreationForm, LecturerUserCreationForm

# Create your views here.

# class signStudentView(CreateView):
#     model = User
#     form_class = StudentUserCreationForm
#     template_name = "accounts/signupStudent.html"


#     def form_invalid(self, form):
#       user = form.save()
#       login(self.request, user)
#       return redirect("HomePage:home")


class signStudentView(View):
    def get(self, request):
        form = StudentUserCreationForm()
        context = {
            "form": form,
        }
        return render(request, "accounts/signupStudent.html", context)

    def post(self, request):
        form = StudentUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("Details:d-s", user.id)
        else:
            return render(request, "accounts/signupStudent.html", {"form": form})


class signLectureView(View):
    def get(self, request):
        form = LecturerUserCreationForm()
        return render(request, "accounts/signupLecture.html", {"form": form})

    def post(self, request):
        form = LecturerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("Details:d-l", user.id)
        else:
            return render(request, "accounts/signupLecture.html", {"form": form})


def signUp(request):
    return render(request, "accounts/signup.html")
