from django.contrib import admin
from django.utils.html import format_html

from .models import Profile, Project, SocialLink


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role", "email", "location", "avatar_preview")
    readonly_fields = ("avatar_preview_large",)

    fieldsets = (
        ("Identity", {"fields": ("full_name", "role", "tagline", "bio")}),
        ("Media", {"fields": ("profile_picture", "avatar_preview_large", "resume")}),
        ("Contact", {"fields": ("email", "location")}),
    )

    def has_add_permission(self, request):
        if Profile.objects.exists():
            return False
        return super().has_add_permission(request)

    def avatar_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="height:42px;width:42px;'
                'object-fit:cover;border-radius:50%;" />',
                obj.profile_picture.url,
            )
        return "—"

    avatar_preview.short_description = "Photo"

    def avatar_preview_large(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="max-height:280px;border-radius:8px;'
                'border:2px solid #6b4423;" />',
                obj.profile_picture.url,
            )
        return "No image uploaded yet."

    avatar_preview_large.short_description = "Preview"


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("icon_preview", "display_label", "platform", "url", "order", "visible")
    list_editable = ("order", "visible")
    list_filter = ("platform", "visible")
    search_fields = ("label", "url")

    def icon_preview(self, obj):
        return format_html(
            '<i class="{}" style="font-size:18px;color:#6b4423;"></i>', obj.icon_class
        )

    icon_preview.short_description = ""

    def display_label(self, obj):
        return obj.display_label

    display_label.short_description = "Label"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "role", "year", "featured", "order")
    list_editable = ("featured", "order")
    list_filter = ("featured", "year")
    search_fields = ("title", "short_description", "role")

    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;width:60px;'
                'object-fit:cover;border-radius:4px;" />',
                obj.image.url,
            )
        return "—"

    thumb.short_description = "Image"