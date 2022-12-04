from django.shortcuts import render, redirect
from django.views import View
from accounts.models import Student, Lecturer, User
from DetailsAccount.form import StudentForm, UserUpdate, LecturerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import base64
from imagekitio import ImageKit
imagekit = ImageKit(
    private_key='private_0InZG7wQykta/PjGyhg2Nk14fAw=',
    public_key='public_wI6Gnx1NNvSxeDBJlqi27qErJO8=',
    url_endpoint='https://ik.imagekit.io/zyae7okkm'
)
# Create your views here.


class DetailsStudentView(View):
    def get(self, request, student_id):
        student = Student.objects.get(pk=student_id)
        userStudent = User.objects.get(pk=student_id)
        print(userStudent.imag_profile)
        form_student = StudentForm(request.POST or None, instance=student)
        form_user = UserUpdate(None, instance=userStudent)
        return render(
            request, "details.html", {"form": form_student, "form_user": form_user}
        )

    def post(self, request, student_id):
        form_student = StudentForm(request.POST, request.FILES)
        if form_student.is_valid():
            first_name = form_student.cleaned_data["first_name"]
            last_name = form_student.cleaned_data["last_name"]
            user = User.objects.get(pk=student_id)
            email = form_student.cleaned_data["email"]
            user.first_name = first_name
            user.last_name = last_name
            img = request.FILES.get("imag_profile")
            if img != None:
                imagekit_url = imagekit.upload_file(
                                    file =  base64.b64encode(img.read()), # required
                                    file_name= img.name, # required
                                )
                user.imag_profile = imagekit_url['response']['name']
            user.save()
            student = Student.objects.get(pk=student_id)
            student.first_name = first_name
            student.last_name = last_name
            student.Phone = form_student.cleaned_data["Phone"]
            student.ID = form_student.cleaned_data["ID"]
            student.department = form_student.cleaned_data["department"]
            student.year = form_student.cleaned_data["year"]
            student.semester = form_student.cleaned_data["semester"]

            student.save()
            return redirect("HomePage:home")
        userStudent = User.objects.get(pk=student_id)
        form_user = UserUpdate(None, instance=userStudent)
        return render(
            request, "details.html", {"form": form_student, "form_user": form_user}
        )


class ChangeStudentPass(View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form_user = UserUpdate(None, instance=user)
        return render(request, "changePass.html", {"form_user": form_user})

    def post(self, request, user_id):
        form = UserUpdate(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=user_id)
            pasw = form.cleaned_data["password"]
            user.set_password(pasw)
            user.save()
            user = authenticate(username=user.username, password=pasw)
            login(request, user)
            return redirect("HomePage:home")
        else:
            return render(request, "changePass.html", {"form_user": form})


# ----------------------------------------------------------------------------------------------------------------------------------------------------


class DetailsLectureView(View):
    def get(self, request, lecturer_id):
        lecturer = Lecturer.objects.get(pk=lecturer_id)
        userLecturer = User.objects.get(pk=lecturer_id)
        form_lecturer = LecturerForm(request.POST or None, instance=lecturer)
        form_user = UserUpdate(None, instance=userLecturer)
        return render(
            request, "details.html", {"form": form_lecturer, "form_user": form_user}
        )

    def post(self, request, lecturer_id):
        form_lecturer = LecturerForm(request.POST, request.FILES)
        if form_lecturer.is_valid():
            first_name = form_lecturer.cleaned_data["first_name"]
            last_name = form_lecturer.cleaned_data["last_name"]
            user = User.objects.get(pk=lecturer_id)
            email = form_lecturer.cleaned_data["email"]
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            img = request.FILES.get("imag_profile")  
            print(img)    
            if img != None:
                imagekit_url = imagekit.upload_file(
                                    file =  base64.b64encode(img.read()), # required
                                    file_name= img.name, # required
                                )
                user.imag_profile = imagekit_url['response']['name']
            user.save()
            lecturer = Lecturer.objects.get(pk=lecturer_id)
            lecturer.first_name = first_name
            lecturer.last_name = last_name
            lecturer.Phone = form_lecturer.cleaned_data["Phone"]
            lecturer.ID = form_lecturer.cleaned_data["ID"]
            lecturer.save()
            return redirect("HomePage:home")
        userLecturer = User.objects.get(pk=lecturer_id)
        form_user = UserUpdate(None, instance=userLecturer)
        return render(
            request, "details.html", {"form": form_lecturer, "form_user": form_user}
        )


def deleteUser(request, user_id):
    user = User.objects.get(pk=user_id)
    user.delete()
    return redirect("HomePage:home")
