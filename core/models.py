from django.core.exceptions import ValidationError
from django.db import models


class Profile(models.Model):
    full_name = models.CharField(max_length=120, default="Shem Okebiro")
    role = models.CharField(max_length=120, default="Designer & Developer")
    tagline = models.CharField(
        max_length=200,
        default="Designing quiet, deliberate interfaces.",
    )
    bio = models.TextField(
        blank=True,
        help_text="Short bio shown under the headline.",
    )
    profile_picture = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True,
        help_text="Used as the full-bleed homepage background.",
    )
    resume = models.FileField(
        upload_to="resume/",
        blank=True,
        null=True,
    )
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=120, blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.full_name

    def clean(self):
        if Profile.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Only one Profile row is allowed. Edit the existing one.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        return cls.objects.first()


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ("github", "GitHub"),
        ("linkedin", "LinkedIn"),
        ("x", "X / Twitter"),
        ("instagram", "Instagram"),
        ("dribbble", "Dribbble"),
        ("behance", "Behance"),
        ("email", "Email"),
        ("website", "Website"),
        ("other", "Other"),
    ]

    ICON_MAP = {
        "github": "fa-brands fa-github",
        "linkedin": "fa-brands fa-linkedin-in",
        "x": "fa-brands fa-x-twitter",
        "instagram": "fa-brands fa-instagram",
        "dribbble": "fa-brands fa-dribbble",
        "behance": "fa-brands fa-behance",
        "email": "fa-solid fa-envelope",
        "website": "fa-solid fa-globe",
        "other": "fa-solid fa-link",
    }

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default="other")
    label = models.CharField(max_length=80, blank=True, help_text="Optional custom label.")
    url = models.CharField(
        max_length=300,
        help_text="Full URL, or mailto: for email.",
    )
    order = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.label or self.get_platform_display()

    @property
    def icon_class(self):
        return self.ICON_MAP.get(self.platform, "fa-solid fa-link")

    @property
    def display_label(self):
        return self.label or self.get_platform_display()


class Project(models.Model):
    title = models.CharField(max_length=160)
    short_description = models.CharField(max_length=280, blank=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    link = models.URLField(blank=True)
    role = models.CharField(max_length=120, blank=True)
    year = models.CharField(max_length=10, blank=True)
    order = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title