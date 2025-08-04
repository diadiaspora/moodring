import requests
from django.shortcuts import render, redirect
# DELETE these three lines entirely:
# from django.contrib.auth.views import LoginView
# from django.contrib.auth import login
# from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, TemplateView
from .models import MoodEntry
import os
from moodring.api import generate_affirmation


MOOD_COLORS = {
    "Happy": "#FFF3B0",        # Soft Yellow
    "Sad": "#A0C4FF",          # Light Blue
    "Angry": "#FFADAD",        # Soft Red
    "Anxious": "#FFE1A8",      # Soft Orange
    "Calm": "#C7F9CC",         # Pale Green
    "Tired": "#D0C7FF",        # Light Lavender
    "Excited": "#FFC6FF",      # Soft Pink
    "Frustrated": "#CABBE9",   # Soft Purple
    "Grateful": "#86F284",     # Light Teal
    "Other": "#E0E0E0",        # Light Gray fallback
}

class Home(TemplateView):
    template_name = "home.html"

class MoodCreate(CreateView):
    model = MoodEntry
    fields = ['mood', 'intensity', 'journal_text']
    # DELETE this entire `def form_valid(self, form):` block
    # from the previous version if it included `form.instance.user = self.request.user`.
    # Make sure it looks like this now:
    def form_valid(self, form):
        mood = form.cleaned_data['mood']
        journal_text = form.cleaned_data['journal_text']
        api_key = os.getenv("GEMINI_API_KEY")

        affirmation = generate_affirmation(api_key, mood, journal_text)

        form.instance.affirmation = affirmation

        return super().form_valid(form)


class MoodUpdate(UpdateView):
    model = MoodEntry
    fields = ['journal_text']
    success_url = '/moods/'

class MoodDelete(DeleteView):
    model = MoodEntry
    success_url = '/moods/'


def moods_index(request):
    moods = MoodEntry.objects.all().order_by('-created_at')

    mood_summary = (
        MoodEntry.objects
        .all()
        .values('mood')
        .annotate(count=Count('mood'))
        .order_by('-count')
    )

    labels = [entry['mood'] for entry in mood_summary]
    data = [entry['count'] for entry in mood_summary]
    colors = [MOOD_COLORS.get(label, "#E0E0E0") for label in labels]

    return render(request, 'moods/index.html', {
    'moods': moods,
    'mood_labels': labels,
    'mood_data': data,
    'mood_colors': colors,
})

def about(request):
    return render(request, "about.html")


# DELETE this entire function. Do not just comment it out.
# def signup(request):
#     error_message = ""
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("moods")
#         else:
#             error_message = "Invalid sign up - try again"
#     form = UserCreationForm()
#     context = {"form": form, "error_message": error_message}
#     return render(request, "signup.html", context)


def mood_detail(request, pk):
    mood = MoodEntry.objects.get(id=pk)

    # Only generate an affirmation if it hasn't already been saved
    if not mood.affirmation:
        api_key = os.getenv("GEMINI_API_KEY")
        journal_text = mood.journal_text or "No journal entry provided."
        affirmation = generate_affirmation(api_key, mood.mood, journal_text)
        mood.affirmation = affirmation
        mood.save()

    return render(request, 'moods/detail.html', {
        'mood': mood,
    })


# DELETE this entire function. Do not just comment it out.
# def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['affirmation'] = self.request.session.pop('affirmation', None)
#         return context