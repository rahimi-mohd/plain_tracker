from django import forms
from django.forms import modelformset_factory
from .models import Comment, Tracker, TrackerImage


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body", "image")


class TrackerForm(forms.ModelForm):
    class Meta:
        model = Tracker
        fields = ["title", "body", "priority", "assigned_to"]


class TrackerImageForm(forms.ModelForm):
    class Meta:
        model = TrackerImage
        fields = ["image"]


# A formset to handle multiple image uploads
TrackerImageFormSet = modelformset_factory(
    TrackerImage,
    form=TrackerImageForm,
    extra=3,  # show 3 empty image fields by default
    can_delete=True,  # allow user to remove images
)
