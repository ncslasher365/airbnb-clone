from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    def count_used_by(self, obj):
        return obj.rooms.count()

    list_display = (
        "name",
        "count_used_by",
    )


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "price", "address")},
        ),
        (
            "Additional Info",
            {
                "fields": (
                    "guests",
                    "beds",
                    "bathrooms",
                    "bedrooms",
                    "check_in",
                    "check_out",
                )
            },
        ),
        (
            "Host Information",
            {"classes": ("collapse",), "fields": ("host", "instant_book")},
        ),
        (
            "Rules, Types, Facilities, Amenities",
            {"fields": ("house_rules", "facilities", "amenities", "room_type")},
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "instant_book",
        "check_in",
        "check_out",
        "count_additional_info",
        "bedrooms",
        "host",
        "count_photos",
        "result_rating",
    )

    list_filter = (
        "host__superhost",
        "instant_book",
        "city",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "country",
    )

    raw_id_fields = ("host",)

    search_fields = ("^city", "^host__username")

    filter_horizontal = ("amenities", "facilities", "house_rules")

    def count_additional_info(self, obj):
        return obj.amenities.count()

    count_additional_info.short_description = "Count Amenities"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"

    inlines = [
        PhotoInline,
    ]


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f"<img width='50px' src='{obj.file.url}'/>")

    get_thumbnail.short_description = "Thumbnail Photo"
