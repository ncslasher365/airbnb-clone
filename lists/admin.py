from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):

    list_display = ("name", "user", "count_stays")

    search_fields = ("name",)

    filter_horizontal = ("places",)
