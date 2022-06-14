from django.http import HttpResponse, HttpResponseRedirect
from projects.models import Project, RequiredProjectFile, UploadedProjectFile
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import AnonymousUser

# Create your views here.

def view(request, url):
    user = request.user
    if user == AnonymousUser():
        return redirect('account_login')
    project = Project.objects.get(user_friendly_url = url)
    users = project.allocated_to.all()
    requiredProjectFiles = RequiredProjectFile.objects.all()
    uploaded_file = dict()
    for requiredProjectFile in requiredProjectFiles:
        try:
            uploadedProjectFile = UploadedProjectFile.objects.get(file_name = requiredProjectFile, project = project)
            uploaded_file[requiredProjectFile.file_name] = uploadedProjectFile.file_name
        except:
            uploaded_file[requiredProjectFile.file_name] = None
    context = {
        'project' : project,
        'users' : users,
        'uploaded_file' : uploaded_file
    }
    return render(request, "projects/view.html", context)

def upload_project_files(request, url, file_name):
    user = request.user
    if user == AnonymousUser():
        return redirect('account_login')
    project = Project.objects.get(user_friendly_url = url)
    requiredProjectFile = RequiredProjectFile.objects.get(file_name = file_name)
    try:
        uploadedProjectFile = UploadedProjectFile.objects.get(file_name = requiredProjectFile, project = project)
    except:
        uploadedProjectFile = None
    context = {
        'project' : project,
        'file_name' : file_name,
        'uploadedProjectFile' : uploadedProjectFile
    }
    if request.method == 'POST':
        fs = FileSystemStorage()
        if request.FILES.get('file', False):
            file = request.FILES['file']
            filename = fs.save(url+'/'+file_name+'/'+file.name, file)
            if uploadedProjectFile:
                uploadedProjectFile.file_name = fs.url(filename)
            else:
                uploadedProjectFile = UploadedProjectFile.objects.create(file_name=requiredProjectFile,
                                                    project = project,
                                                    file = filename,
                                                    uploaded_by = request.user)
            uploadedProjectFile.save()
        return HttpResponseRedirect('/project/'+url)
    return render(request, "projects/upload_file.html", context)