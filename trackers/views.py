from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .models import Tracker, TrackerImage
from .forms import CommentForm, TrackerForm, ImageUploadForm


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


# ----------------------------
# Tracker List Views
# ----------------------------
class TrackerListView(LoginRequiredMixin, ListView):
    model = Tracker
    template_name = "trackers/tracker_list.html"

    def get_queryset(self):
        return Tracker.objects.exclude(status="drop")


class MyTrackerListView(ListView):
    model = Tracker
    template_name = "trackers/my_tracker.html"

    def get_queryset(self):
        return Tracker.objects.filter(
            (Q(author=self.request.user) | Q(assigned_to=self.request.user))
            & ~Q(status="drop")
        )


class DroppedListView(ListView):
    model = Tracker
    template_name = "trackers/dropped_tracker.html"

    def get_queryset(self):
        base_dropped = Tracker.objects.filter(status="drop")
        if self.request.user.is_staff:
            return base_dropped
        else:
            return base_dropped.filter(
                Q(author=self.request.user) | Q(assigned_to=self.request.user)
            )


# ----------------------------
# Tracker Detail / Comments
# ----------------------------
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
        tracker = self.object
        return reverse("tracker_detail", kwargs={"pk": tracker.pk})


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
        """
        Add the image upload form to the context.
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["image_form"] = ImageUploadForm(
                self.request.POST, self.request.FILES
            )
        else:
            context["image_form"] = ImageUploadForm()
        return context

    def form_valid(self, form):
        """
        Save Tracker and all uploaded images with validation.
        """
        form.instance.author = self.request.user
        form.instance.status = "in_progress"

        image_form = ImageUploadForm(self.request.POST, self.request.FILES)

        # Validate both forms
        if form.is_valid() and image_form.is_valid():
            self.object = form.save()

            # Save uploaded images
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

            # Render template with form errors
            context = self.get_context_data(form=form)
            context["image_form"] = image_form
            return self.render_to_response(context)


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
