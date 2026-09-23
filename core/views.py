from django.shortcuts import render

from .models import Profile, Project, SocialLink


def home(request):
    profile = Profile.get_solo()
    social_links = SocialLink.objects.filter(visible=True)
    projects = Project.objects.all()

    context = {
        "profile": profile,
        "social_links": social_links,
        "projects": projects,
    }
    return render(request, "core/home.html", context)