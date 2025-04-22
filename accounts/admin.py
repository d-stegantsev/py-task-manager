from django.contrib import admin

from accounts.models import Position, Worker


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "position")
    search_fields = ("username", "email")
    list_filter = ("position",)
