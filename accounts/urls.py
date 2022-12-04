from django.urls import path


from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signUp, name="signup"),
    path("signupStudent/", views.signStudentView.as_view(), name="si-student"),
    path("signupLecture/", views.signLectureView.as_view(), name="si-lecture"),
    # path('login/', views.LogInView.as_view(), name='logIn'),
]
