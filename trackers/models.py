from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.
class Tracker(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("normal", "Normal"),
        ("high", "High"),
    ]

    STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("done", "Done"),
        ("drop", "Drop"),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_trackers",
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="normal",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_progress",
    )
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tracker_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    trackers = models.ForeignKey(
        "Tracker",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse("tracker_detail", kwargs={"pk": self.tracker.pk})
