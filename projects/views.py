from projects.models import Project
from django.shortcuts import render

# Create your views here.

def view(request, url):
    project = Project.objects.get(user_friendly_url = url)
    users = project.allocated_to.all()
    context = {
        'project' : project,
        'users' : users,
    }
    return render(request, "projects/view.html", context)