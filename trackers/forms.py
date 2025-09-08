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


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class ImageUploadForm(forms.Form):
    images = forms.FileField(
        widget=MultiFileInput(attrs={"class": "form-control"}),
        required=False,
        label="Upload Images",
        help_text="You can attach max of 5 images",
    )

    def clean_images(self):
        files = self.files.getlist("images")
        if len(files) > 5:
            raise forms.ValidationError(
                "You can upload a maximum of 5 images at a time."
            )
        return files
