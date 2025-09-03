from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.contrib.auth import get_user_model

from trackers.models import Tracker
from .forms import CustomUserCreationForm


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


User = get_user_model()


class ProfileDetailView(DetailView):
    model = User
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        context["active_count"] = Tracker.objects.filter(
            author=user, status="in_progress"
        ).count()
        context["done_count"] = Tracker.objects.filter(
            author=user, status="done"
        ).count()
        context["dropped_count"] = Tracker.objects.filter(
            author=user, status="drop"
        ).count()

        return context
