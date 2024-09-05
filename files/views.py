from django.contrib.sites import requests

from django.shortcuts import render

from .forms import  UploadForm

from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from .models import UserFile
import mimetypes
import requests



@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            user_file = form.save(commit=False)
            user_file.user = request.user  # Прив'язуємо файл до поточного користувача
            user_file.save()
            return redirect('file_list')
    else:
        form = UploadForm()
    return render(request, 'files/upload_file.html', {'form': form})


@login_required
def file_list(request):

    category = request.GET.get('category', 'all')

    if category == 'all':
        files = UserFile.objects.filter(user=request.user)
    else:
        files = UserFile.objects.filter(user=request.user, category=category)

    context = {
        'files': files,
        'category': category,
    }
    return render(request, 'files/file_list.html', context)

@login_required
def download_file(request, file_id):
    file = get_object_or_404(UserFile, id=file_id, user=request.user)
    file_url = file.file.url

    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        file_mimetype, _ = mimetypes.guess_type(file.file.name)
        django_response = HttpResponse(response.content, content_type=file_mimetype)
        django_response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'

        return django_response
    except requests.exceptions.RequestException as e:
        print(f"Помилка доступу або конфігурації: {e}")
        raise Http404("Файл не знайдено або недоступний.")


@login_required
def delete_file(request, file_id):
    file = get_object_or_404(UserFile, id=file_id, user=request.user)
    file.file.delete(save=False)
    file.delete()
    return redirect('file_list')