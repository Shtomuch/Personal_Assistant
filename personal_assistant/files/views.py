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


# @login_required
# def image_upload(request):
#     if request.method == 'POST':
#         image_file = request.FILES['image_file']
#         image_type = request.POST['image_type']
#         if settings.USE_SPACES:
#             if image_type == 'private':
#                 upload = UploadPrivate(file=image_file)
#             else:
#                 upload = Upload(file=image_file)
#             upload.save()
#             image_url = upload.file.url
#         else:
#             fs = FileSystemStorage()
#             filename = fs.save(image_file.name, image_file)
#             image_url = fs.url(filename)
#         return render(request, 'files/upload.html', {
#             'image_url': image_url
#         })
#     return render(request, 'files/upload.html')  # Змініть шлях до шаблону
#
# @login_required
# def file_list(request):
#     category = request.GET.get('category', 'all')
#     if category == 'all':
#         files = UserFile.objects.filter(user=request.user)  # Фільтрує файли поточного користувача
#     else:
#         files = UserFile.objects.filter(user=request.user, category=category)
#     return render(request, 'files/file_list.html', {'files': files, 'category': category})
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
    files = UserFile.objects.filter(user=request.user)  # Відображаємо лише файли поточного користувача
    return render(request, 'files/file_list.html', {'files': files})


@login_required
def download_file(request, file_id):
    # Знайти файл користувача
    file = get_object_or_404(UserFile, id=file_id, user=request.user)

    # Отримати URL файлу з хмарного сховища
    file_url = file.file.url

    try:
        # Отримати файл за допомогою HTTP-запиту
        response = requests.get(file_url, stream=True)
        response.raise_for_status()  # Перевірити, чи запит був успішним

        # Визначити MIME тип файлу
        file_mimetype, _ = mimetypes.guess_type(file.file.name)

        # Повернути файл як завантаження з оригінальним іменем
        django_response = HttpResponse(response.content, content_type=file_mimetype)
        django_response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'

        return django_response
    except requests.exceptions.RequestException as e:
        print(f"Помилка доступу або конфігурації: {e}")
        raise Http404("Файл не знайдено або недоступний.")


@login_required
def delete_file(request, file_id):
    file = get_object_or_404(UserFile, id=file_id, user=request.user)  # Отримання файлу користувача
    file.file.delete(save=False)  # Видалення файлу з хмарного сховища
    file.delete()  # Видалення запису з бази даних
    return redirect('file_list')