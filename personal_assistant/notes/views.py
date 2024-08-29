from django.shortcuts import render, redirect
from notes.forms import NoteForm
from notes.models import Notes

def creationView(request):
    form = NoteForm
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("/main")
    template_name = 'notes/note.html'
    context = {'form': form}
    return render(request, template_name, context)

def showView(request):
    obj = Notes.objects.all()
    template_name = 'notes/show.html'
    context = {'obj': obj}
    return render(request, template_name, context)

def updateView(request, f_id):
    obj = Notes.objects.get(id=f_id)
    form = NoteForm(instance=obj)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/main')
    template_name = 'notes/note.html'
    context = {'form': form}
    return render(request, template_name, context)

def deleteView(request, f_id):
    obj = Notes.objects.get(id=f_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('/main')
    template_name = 'notes/confirm.html'
    context = {'obj': obj}
    return render(request, template_name, context)


