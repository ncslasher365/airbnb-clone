from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from rooms.models import Room

# Register your models here.


class RoomInline(admin.TabularInline):
    model = Room


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Fields",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                    "login_method",
                )
            },
        ),
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "login_method",
    )

    list_filter = UserAdmin.list_filter + ("superhost", "login_method")

    inlines = [
        RoomInline,
    ]

    # list_display = (  # displaying database fields inside django administration panel
    #     "username",
    #     "gender",
    #     "email",
    #     "language",
    #     "currency",
    #     "superhost",
    # )
    # list_filter = ("superhost", "language", "currency")


# admin.site.register(models.User, CustomUserAdmin)
