from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse

from .models import Tracker
from .forms import CommentForm


# Create your views here.
class TrackerListView(LoginRequiredMixin, ListView):
    model = Tracker
    template_name = "trackers/tracker_list.html"


class CommentGet(LoginRequiredMixin, DetailView):
    model = Tracker
    template_name = "trackers/tracker_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):
    model = Tracker
    form_class = CommentForm
    template_name = "trackers/tracker_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.trackers = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        tracker = self.object
        return reverse("tracker_detail", kwargs={"pk": tracker.pk})


class TrackerDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


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
