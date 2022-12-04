from django.shortcuts import redirect, render
from django.views import View
from category.models import HomeWork, YouTubeVideo
from category.form import CourseForm, HomeWorkForm, CreatCourseForm, CommentHomeWorkForm
from category.models import Course, CommentHomeWork
from accounts.models import Student, User
from imagekitio import ImageKit
import base64

imagekit = ImageKit(
    private_key="private_0InZG7wQykta/PjGyhg2Nk14fAw=",
    public_key="public_wI6Gnx1NNvSxeDBJlqi27qErJO8=",
    url_endpoint="https://ik.imagekit.io/zyae7okkm",
)

# Create your views here.


class CategoryView(View):
    def get(self, request, user_id):
        form = CourseForm()
        if request.user.is_student:
            user = User.objects.get(pk=user_id)
            student = Student.objects.get(user=user)
            form = CourseForm(instance=student)
        return render(request, "category.html", {"form": form})

    def post(self, request, user_id):
        form = CourseForm(request.POST)
        if form.is_valid():
            depart = form.cleaned_data["department"]
            year = form.cleaned_data["year"]
            semester = form.cleaned_data["semester"]
            kind_of = form.cleaned_data["kind_of"]
            if Course.objects.filter(
                department=depart, year=year, semester=semester, kind_of=kind_of
            ).exists():
                all_courses = Course.objects.filter(
                    department=depart, year=year, semester=semester, kind_of=kind_of
                ).values()
                return render(
                    request, "category.html", {"form": form, "all_courses": all_courses}
                )
            else:
                return render(
                    request,
                    "category.html",
                    {"error": "No results have been found", "form": form},
                )

        return render(request, "category.html", {"form": form})


class HomeWorksView(View):
    def get(self, request, course_id, user_id):
        if bool(request.GET):
            value = request.GET["selecting"]
            if value == "1":
                course = Course.objects.get(id=course_id)
                homeworks = (
                    HomeWork.objects.filter(course=course, ratings__isnull=False)
                ).order_by("-ratings__average")
                mylist = list(dict.fromkeys(homeworks))
                return render(
                    request,
                    "HomeWorks.html",
                    {"course": course, "homeworks": mylist, "1": "1"},
                )
            elif value == "2":
                course = Course.objects.get(id=course_id)
                homeworks = (HomeWork.objects.filter(course=course)).order_by(
                    "-nameFile"
                )
                return render(
                    request,
                    "HomeWorks.html",
                    {"course": course, "homeworks": homeworks, "2": "2"},
                )
            else:
                course = Course.objects.get(id=course_id)
                homeworks = HomeWork.objects.filter(course=course)
                return render(
                    request,
                    "HomeWorks.html",
                    {"course": course, "homeworks": homeworks},
                )
        else:
            course = Course.objects.get(id=course_id)
            homeworks = HomeWork.objects.filter(course=course)
        return render(
            request, "HomeWorks.html", {"course": course, "homeworks": homeworks}
        )


class UploadFileView(View):
    """
    UploadFileView
    """

    def get(self, request, course_id, user_id):
        form = HomeWorkForm(initial={"course": course_id})
        return render(request, "upload_file.html", {"form": form})

    def post(self, request, course_id, user_id):
        form = HomeWorkForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            file = request.FILES.get("file")
            imagekit_url = imagekit.upload_file(
                file=base64.b64encode(file.read()),  # required
                file_name=file.name,  # required
            )
            homework = HomeWork.objects.create(
                nameFile=form.cleaned_data["nameFile"],
                file=imagekit_url["response"]["name"],
                course=form.cleaned_data["course"],
                user=user,
            )
            homework.save()
            return redirect("Category:homework", course_id, user_id)
        return render(request, "upload_file.html", {"form": form})


class CreateCourseView(View):
    def get(self, request):
        form = CourseForm()
        folder = CreatCourseForm()
        return render(
            request, "category.html", {"folder": folder, "form": form, "test": "test"}
        )

    def post(self, request):
        form = CreatCourseForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("Category:cat", request.user.id)


def deleteCourse(request, course_id):
    course = Course.objects.get(pk=course_id)
    course.delete()
    return redirect("Category:cat", request.user.id)


def deleteFile(request, course_id, hw_id):
    hw = HomeWork.objects.get(pk=hw_id)
    hw.delete()
    return redirect("Category:homework", course_id, request.user.id)


class VideoView(View):
    """
    VideoView
    """

    def get(self, request, course_id):
        if bool(request.GET):
            value = request.GET["selecting"]
            if value == "1":
                course = Course.objects.get(id=course_id)
                videos = (
                    YouTubeVideo.objects.filter(course=course, ratings__isnull=False)
                ).order_by("-ratings__average")
                mylist = list(dict.fromkeys(videos))
                return render(
                    request, "videos.html", {"course": course, "videos": mylist}
                )
            elif value == "2":
                course = Course.objects.get(id=course_id)
                videos = (YouTubeVideo.objects.filter(course=course)).order_by("-title")
                return render(
                    request, "videos.html", {"course": course, "videos": videos}
                )
        else:
            course = Course.objects.get(id=course_id)
            videos = YouTubeVideo.objects.filter(course=course)
        return render(request, "videos.html", {"course": course, "videos": videos})



class ForumFileView(View):
    """
    ForumFileView
    """

    def get(self, request, hw_id):
        hw = HomeWork.objects.get(pk=hw_id)
        comments = CommentHomeWork.objects.filter(hw=hw).iterator()
        comment = CommentHomeWorkForm()
        return render(
            request,
            "ForumFile.html",
            {"hw": hw, "comments": comments, "form_comment": comment},
        )

    def post(self, request, hw_id):
        form = CommentHomeWorkForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            hw = HomeWork.objects.get(pk=hw_id)
            comment = CommentHomeWork.objects.create(
                user=user, hw=hw, message=form.cleaned_data["message"]
            )
            comment.save()
        return redirect("Category:forum-file", hw_id)


def DeleteComment(request, comment_id, hw_id):
    """
    DeleteComment
    """
    comment = CommentHomeWork.objects.get(pk=comment_id)
    comment.delete()
    return redirect("Category:forum-file", hw_id)


def deleteVideo(request, course_id, video_id):
    video = YouTubeVideo.objects.get(id=video_id)
    video.delete()
    return redirect("Category:videos", course_id)
