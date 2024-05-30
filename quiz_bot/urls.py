from django.contrib import admin
from django.urls import path, include
from core.views import chat, start_quiz, reset_quiz  # Import views from the app

urlpatterns = [
    path("", chat, name="chat"),
    path("start_quiz/", start_quiz, name="start_quiz"),
    path("reset_quiz/", reset_quiz, name="reset_quiz"),
    # path("admin/", admin.site.urls),
]