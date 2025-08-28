from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Tracker


# Create your views here.
class TrackerListView(LoginRequiredMixin, ListView):
    model = Tracker
    template_name = "trackers/tracker_list.html"


class TrackerDetailView(LoginRequiredMixin, DetailView):
    model = Tracker
    template_name = "trackers/tracker_detail.html"


class TrackerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tracker
    fields = ("body", "priority", "status", "assigned_to")
    template_name = "trackers/tracker_edit.html"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class TrackerDeleteView(LoginRequiredMixin, DeleteView):
    model = Tracker
    template_name = "trackers/tracker_delete.html"
    success_url = reverse_lazy("tracker_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class TrackerCreateView(LoginRequiredMixin, CreateView):
    model = Tracker
    template_name = "trackers/tracker_new.html"
    fields = (
        "title",
        "body",
        "priority",
        "assigned_to",
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = "Open"
        return super().form_valid(form)
