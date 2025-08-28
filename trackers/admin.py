from django.contrib import admin

from .models import Tracker, Comment


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0


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
