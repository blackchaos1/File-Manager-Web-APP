# files/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from .models import UserFile, UserProfile
from .forms import UserFileForm
import os
from django.shortcuts import render, redirect, get_object_or_404
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            user_file = form.save(commit=False)
            user_profile = UserProfile.objects.get(user=request.user)
            user_file.user = request.user
            user_file.company = user_profile.company
            user_file.save()
            return redirect('file_list')
    else:
        form = UserFileForm()
    return render(request, 'files/upload_file.html', {'form': form})

@login_required
def file_list(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        files = UserFile.objects.filter(company=user_profile.company,)
        return render(request, 'files/file_list.html', {'files': files})
    except:
        return render(request, 'files/file_list_404.html')

@login_required
def download_file(request, file_id):
    user_profile = UserProfile.objects.get(user=request.user)
    try:
        user_file = UserFile.objects.get(id=file_id, company=user_profile.company)
    except UserFile.DoesNotExist:
        raise Http404
    file_path = user_file.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    raise Http404
