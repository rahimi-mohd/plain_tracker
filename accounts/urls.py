from django.urls import path

from .views import SignUpView, ProfileDetailView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("<int:pk>/profile/", ProfileDetailView.as_view(), name="profile"),
]
