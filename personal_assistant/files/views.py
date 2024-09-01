from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm
from .models import UserFile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import mimetypes
from django.shortcuts import redirect

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user  # Прив'язка файлу до користувача
            file.save()
            return redirect('file_list')  # Перенаправлення на список файлів користувача
    else:
        form = FileUploadForm()
    return render(request, 'files/upload_file.html', {'form': form})

@login_required
def file_list(request):
    category = request.GET.get('category', 'all')
    if category == 'all':
        files = UserFile.objects.filter(user=request.user)  # Фільтрує файли поточного користувача
    else:
        files = UserFile.objects.filter(user=request.user, category=category)
    return render(request, 'files/file_list.html', {'files': files, 'category': category})



@login_required
def download_file(request, file_id):
    file = get_object_or_404(UserFile, id=file_id, user=request.user)
    file_path = file.file.path
    file_mimetype, _ = mimetypes.guess_type(file_path)

    response = HttpResponse(file.file, content_type=file_mimetype)
    response['Content-Disposition'] = f'attachment; filename="{file.title}"'
    return response


@login_required
def delete_file(request, file_id):
    file = get_object_or_404(UserFile, id=file_id, user=request.user)  # Файл користувача
    file.delete()
    return redirect('file_list')