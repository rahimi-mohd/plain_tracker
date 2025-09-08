from django.contrib import admin

from .models import Tracker, Comment, TrackerImage


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0


class TrackerImageInline(admin.TabularInline):
    model = TrackerImage
    extra = 1


class TrackerAdmin(admin.ModelAdmin):
    inlines = [
        CommentInLine,
    ]
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
admin.site.register(Comment)
admin.site.register(TrackerImage)
