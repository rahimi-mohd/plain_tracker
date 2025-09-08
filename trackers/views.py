from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .models import Tracker, TrackerImage
from .forms import CommentForm, TrackerForm, ImageUploadForm


# ----------------------------
# Comments
# ----------------------------
def add_comment(request, pk):
    tracker = get_object_or_404(Tracker, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.tracker = tracker
            comment.author = request.user
            comment.save()
            return render(
                request, "trackers/partials/comment_item.html", {"comment": comment}
            )
    else:
        form = CommentForm()

    return render(
        request,
        "trackers/partials/comment_form.html",
        {"form": form, "tracker": tracker},
    )


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
        comment.tracker = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tracker_detail", kwargs={"pk": self.object.pk})


class TrackerDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


# ----------------------------
# Tracker Create / Update / Delete
# ----------------------------
class TrackerCreateView(LoginRequiredMixin, CreateView):
    model = Tracker
    form_class = TrackerForm
    template_name = "trackers/tracker_new.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image_form"] = (
            ImageUploadForm(self.request.POST, self.request.FILES)
            if self.request.POST
            else ImageUploadForm()
        )
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = "in_progress"

        image_form = ImageUploadForm(self.request.POST, self.request.FILES)

        if form.is_valid() and image_form.is_valid():
            self.object = form.save()
            images = self.request.FILES.getlist("images")
            for image in images:
                TrackerImage.objects.create(tracker=self.object, image=image)

            messages.success(self.request, "Task created successfully!")
            return redirect(self.object.get_absolute_url())
        else:
            if image_form.errors.get("images"):
                for err in image_form.errors["images"]:
                    messages.error(self.request, err)
            for field, errors in form.errors.items():
                for err in errors:
                    messages.error(self.request, f"{field}: {err}")

            context = self.get_context_data(form=form)
            context["image_form"] = image_form
            return self.render_to_response(context)


class TrackerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tracker
    fields = ("body", "priority", "status", "assigned_to")
    template_name = "trackers/tracker_edit.html"

    def test_func(self):
        return self.get_object().author == self.request.user


class TrackerDeleteView(LoginRequiredMixin, DeleteView):
    model = Tracker
    template_name = "trackers/tracker_delete.html"
    success_url = reverse_lazy("all_issues")

    def test_func(self):
        return self.get_object().author == self.request.user


# ----------------------------
# Unified Issues View (All / My / Dropped)
# ----------------------------
class AllIssuesView(LoginRequiredMixin, TemplateView):
    template_name = "trackers/all_issues.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_type = self.request.GET.get("filter", "all")

        if filter_type == "my":
            context["tracker_list"] = Tracker.objects.filter(
                Q(author=self.request.user) | Q(assigned_to=self.request.user)
            ).exclude(status="drop")
        elif filter_type == "dropped":
            qs = Tracker.objects.filter(status="drop")
            if not self.request.user.is_staff:
                qs = qs.filter(
                    Q(author=self.request.user) | Q(assigned_to=self.request.user)
                )
            context["tracker_list"] = qs
        else:
            context["tracker_list"] = Tracker.objects.exclude(status="drop")

        # HTMX partial rendering
        if self.request.headers.get("HX-Request"):
            self.template_name = "trackers/partials/task_list_partial.html"

        return context
