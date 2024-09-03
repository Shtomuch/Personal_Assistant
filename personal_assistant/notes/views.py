from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from notes.models import Tag

from notes.forms import NoteForm, TagCreateForm
from notes.models import Notes


class CreateNoteView(LoginRequiredMixin, CreateView):
    model = Notes
    template_name = 'notes/note.html'
    form_class = NoteForm
    success_url = reverse_lazy('main_url')

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        response = super().form_valid(form)
        form.instance.tags.set(form.cleaned_data['tags'])

        return response

    def get_success_url(self):
        return reverse_lazy('main_url')


class ShowNoteView(LoginRequiredMixin, DetailView):
    model = Notes
    template_name = 'notes/show.html'
    context_object_name = 'note'

    def get_object(self):
        return Notes.objects.get(id=self.kwargs['f_id'])


class UpdateNoteView(LoginRequiredMixin, UpdateView):
    model = Notes
    form_class = NoteForm
    template_name = 'notes/note.html'
    success_url = reverse_lazy('main_url')

    def get_object(self, queryset=None):
        return Notes.objects.get(id=self.kwargs['f_id'])

    def form_valid(self, form):
        return super().form_valid(form)


class DeleteNoteView(LoginRequiredMixin, DeleteView):
    model = Notes
    template_name = 'notes/delete.html'
    context_object_name = 'note'
    success_url = reverse_lazy('main_url')

    def get_object(self, queryset=None):
        return Notes.objects.get(id=self.kwargs['f_id'])


class MainView(LoginRequiredMixin, ListView):
    model = Notes
    template_name = 'notes/main.html'
    context_object_name = 'notes'

    def get_queryset(self):
        queryset = Notes.objects.filter(user_id=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(tags__name__iexact=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class AddTagView(LoginRequiredMixin, CreateView):
    model = Tag
    template_name = 'notes/add_tag.html'
    success_url = reverse_lazy('create_url')
    form_class = TagCreateForm

    def get_queryset(self):
        return Notes.objects.filter(user_id=self.request.user)



