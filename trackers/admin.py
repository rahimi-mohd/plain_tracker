from django.contrib import admin

from .models import Tracker


class TrackerAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "body",
        "author",
        "assigned_to",
        "priority",
        "status",
        "date",
        "updated_at",
    ]


# Register your models here.
admin.site.register(Tracker, TrackerAdmin)
