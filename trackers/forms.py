from django import forms
from django.forms import modelformset_factory

from .models import Comment, Tracker, TrackerImage


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)


class TrackerForm(forms.ModelForm):
    class Meta:
        model = Tracker
        fields = ["title", "body", "priority"]


class TrackerImageForm(forms.ModelForm):
    class Meta:
        model = TrackerImage
        fields = ["image"]


TrackerImageFormSet = modelformset_factory(
    TrackerImage,
    form=TrackerImageForm,
    extra=3,
    can_delete=True,
)
