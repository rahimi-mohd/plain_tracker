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
from .forms import CommentForm, TrackerForm, TrackerImageFormSet


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
        if self.request.POST:
            context["image_formset"] = TrackerImageFormSet(
                self.request.POST,
                self.request.FILES,
                queryset=TrackerImage.objects.none(),
            )
        else:
            context["image_formset"] = TrackerImageFormSet(
                queryset=TrackerImage.objects.none()
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context["image_formset"]

        form.instance.author = self.request.user
        form.instance.status = "in_progress"

        if form.is_valid() and image_formset.is_valid():
            self.object = form.save()

            # Save images
            for image_form in image_formset:
                if image_form.cleaned_data.get("image"):
                    TrackerImage.objects.create(
                        tracker=self.object, image=image_form.cleaned_data["image"]
                    )

            messages.success(self.request, "Task created successfully!")
            return redirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


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
            # Show only my active tasks (exclude done & dropped)
            context["tracker_list"] = Tracker.objects.filter(
                Q(author=self.request.user) | Q(assigned_to=self.request.user)
            ).exclude(status__in=["drop", "done"])

        elif filter_type == "dropped":
            # Show dropped tasks
            qs = Tracker.objects.filter(status="drop")
            if not self.request.user.is_staff:
                qs = qs.filter(
                    Q(author=self.request.user) | Q(assigned_to=self.request.user)
                )
            context["tracker_list"] = qs

        elif filter_type == "done":
            # Show completed tasks
            qs = Tracker.objects.filter(status="done")
            if not self.request.user.is_staff:
                qs = qs.filter(
                    Q(author=self.request.user) | Q(assigned_to=self.request.user)
                )
            context["tracker_list"] = qs

        else:
            # Default "all" = only active tasks (exclude done & dropped)
            context["tracker_list"] = Tracker.objects.exclude(
                status__in=["drop", "done"]
            )

        # HTMX partial rendering
        if self.request.headers.get("HX-Request"):
            self.template_name = "trackers/partials/task_list_partial.html"

        return context
