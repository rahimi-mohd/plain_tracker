from django.views.generic import ListView

from .models import Tracker


# Create your views here.
class TrackerListView(ListView):
    model = Tracker
    template_name = "trackers/tracker_list.html"
