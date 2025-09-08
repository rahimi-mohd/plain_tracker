from django.urls import path
from .views import (
    TrackerDetailView,
    TrackerUpdateView,
    TrackerDeleteView,
    TrackerCreateView,
    AllIssuesView,
    add_comment,
)

urlpatterns = [
    path("<int:pk>/", TrackerDetailView.as_view(), name="tracker_detail"),
    path("<int:pk>/edit/", TrackerUpdateView.as_view(), name="tracker_edit"),
    path("<int:pk>/delete/", TrackerDeleteView.as_view(), name="tracker_delete"),
    path("new/", TrackerCreateView.as_view(), name="tracker_new"),
    path("all-issues/", AllIssuesView.as_view(), name="all_issues"),
    path("<int:pk>/add-comment/", add_comment, name="add_comment"),
]
