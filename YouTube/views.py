from django.shortcuts import render, redirect
from django.views import View
import requests
from django.conf import settings
from YouTube.models import YouTube
from YouTube.form import CourseForm, CreatCourseForm, YouTubeVideoForm
from category.models import Course, YouTubeVideo
from accounts.models import User

# Create your views here.

SEARCH = ""


class SearchVideoView(View):
    def get(self, request):
        YouTube.objects.all().delete()
        return render(request, "youtube.html")

    def post(self, request):
        SEARCH = request.POST["search"]
        if SEARCH != "":
            search_url = "https://www.googleapis.com/youtube/v3/search"
            video_url = "https://www.googleapis.com/youtube/v3/videos"
            channel_url = "https://www.googleapis.com/youtube/v3/channels?part=snippet&id='+commaSeperatedList+'&fields=items(id%2Csnippet%2Fthumbnails)&key={}".format(
                settings.YOUTUBE_DATA_API_KEY
            )
            para_search = {
                "part": "snippet",
                "q": SEARCH,
                "key": settings.YOUTUBE_DATA_API_KEY,
                "maxResults": 9,
                "type": "video",
            }

            search_response = requests.get(search_url, params=para_search)
            results = search_response.json()["items"]
            ids = []
            for result in results:
                ids.append(result["id"]["videoId"])

            para_videos = {
                "part": "snippet",
                "key": settings.YOUTUBE_DATA_API_KEY,
                "id": ",".join(ids),
            }
            video_response = requests.get(video_url, params=para_videos)
            results = video_response.json()["items"]

            dict_youtube = {}
            list_youtube = []
            channelIdList = []
            for result in results:
                dict_youtube = {
                    "title": result["snippet"]["title"],
                    "thumbnails": result["snippet"]["thumbnails"]["high"]["url"],
                    "channelId": result["snippet"]["channelId"],
                    "IdVideo": result["id"],
                }
                channelIdList.append(result["snippet"]["channelId"])
                list_youtube.append(dict_youtube)

            param_channel = {
                "part": "snippet,contentDetails,statistics",
                "key": settings.YOUTUBE_DATA_API_KEY,
                "id": ",".join(channelIdList),
            }
            channel_response = requests.get(channel_url, params=param_channel)
            results = channel_response.json()["items"]
            profile = []
            profile_dic = {}
            i = 0
            for result in results:
                profile_dic = {
                    "index": i + 1,
                    "channelId": result["id"],
                    "profile": result["snippet"]["thumbnails"]["default"]["url"],
                }
                i += 1
                profile.append(profile_dic)
            new_list = []

            for dic in profile:
                vids = filter(
                    lambda yt: yt["channelId"] == dic["channelId"], list_youtube
                )
                for vid in vids:
                    dic.update(vid)
                new_list.append(dic)

            for lst in new_list:
                YouTube.objects.create(
                    index=lst["index"],
                    channelId=lst["channelId"],
                    IdVideo=lst["IdVideo"],
                    profile=lst["profile"],
                    title=lst["title"],
                    thumbnails=lst["thumbnails"],
                ).save()

            return render(request, "youtube.html", {"videos": new_list})
        return render(request, "youtube.html", {"Empty": "אנא מלא את השדה"})



class SaveVideoView(View):
    def get(self, request, video_index):
        form_course = CourseForm(initial={"kind_of": "5"})
        return render(
            request, "save.html", {"form": form_course, "video_index": video_index}
        )

    def post(self, request, video_index):
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
                    request,
                    "save.html",
                    {
                        "form": form,
                        "all_courses": all_courses,
                        "video_index": video_index,
                    },
                )
            else:
                return render(
                    request,
                    "save.html",
                    {
                        "error": "No results have been found",
                        "form": form,
                        "video_index": video_index,
                    },
                )
        return render(request, "save.html", {"form": form, "video_index": video_index})


class CreateCourseView(View):
    def get(self, request, video_index):
        folder = CreatCourseForm(initial={"kind_of": "5"})
        form = CourseForm(initial={"kind_of": "5"})
        return render(
            request,
            "save.html",
            {"folder": folder, "form": form, "video_index": video_index},
        )

    def post(self, request, video_index):
        form = CreatCourseForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("YouTube:save-video", video_index)


class YouTubeVideoView(View):
    def get(self, request, course_id, user_id, video_index):
        youtube = YouTube.objects.filter(index=video_index).first()
        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)
        form = YouTubeVideoForm(
            initial={"course": course, "user": user}, instance=youtube
        )
        return render(
            request,
            "YoTubeVideo.html",
            {
                "course_id": course_id,
                "user_id": user_id,
                "video_index": video_index,
                "form": form,
            },
        )

    def post(self, request, course_id, user_id, video_index):
        form = YouTubeVideoForm(request.POST)
        print(request.POST)
        if form.is_valid():
            id = YouTubeVideo.objects.count() + 1
            user = User.objects.get(id=user_id)
            course = Course.objects.get(id=course_id)
            you = YouTubeVideo.objects.create(
                id=id,
                user=user,
                course=course,
                channelId=form.cleaned_data["channelId"],
                IdVideo=form.cleaned_data["IdVideo"],
                profile=form.cleaned_data["profile"],
                title=form.cleaned_data["title"],
                thumbnails=form.cleaned_data["thumbnails"],
            )
            print("check")
            return redirect("Category:cat", user_id)
        return render(
            request,
            "YoTubeVideo.html",
            {
                "course_id": course_id,
                "user_id": user_id,
                "video_index": video_index,
                "form": form,
            },
        )
