from django.urls import path

from .views import (
    TrackerListView,
    TrackerDetailView,
    TrackerUpdateView,
    TrackerDeleteView,
    TrackerCreateView,
    MyTrackerListView,
)

urlpatterns = [
    path("<int:pk>/", TrackerDetailView.as_view(), name="tracker_detail"),
    path("<int:pk>/edit/", TrackerUpdateView.as_view(), name="tracker_edit"),
    path("<int:pk>/delete/", TrackerDeleteView.as_view(), name="tracker_delete"),
    path("new/", TrackerCreateView.as_view(), name="tracker_new"),
    path("", TrackerListView.as_view(), name="tracker_list"),
    path("my_tracker/", MyTrackerListView.as_view(), name="my_tracker"),
]
