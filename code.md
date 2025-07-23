




```python
from django.urls import path
from . import views  # Import views to connect routes to view functions

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("about/", views.about, name="about"),
    path("accounts/signup/", views.signup, name="signup"),
    path('moods/', views.moods_index, name='moods'),
    path('moods/create/', views.MoodCreate.as_view(), 
    name='mood-create'),
    path('moods/<int:pk>/', views.mood_detail, 
    name='mood-detail'),
    path('moods/<int:pk>/update/',   
    views.MoodUpdate.as_view(), name='mood-update'),
    path('moods/<int:pk>/delete/', 
    views.MoodDelete.as_view(), name='mood-delete'),
]
```







```python
INTENSITY_LEVEL = (
    ("1", "Subtle"),
    ("2", "Mild"),
    ("3", "Moderate"),
    ("4", "Strong"),
    ("5", "Intense"),
)

MOOD_CHOICES = [
    ("Happy", "Happy 😊"),
    ("Sad", "Sad 😢"),
    ("Angry", "Angry 😠"),
    ("Anxious", "Anxious 😰"),
    ("Calm", "Calm 😌"),
    ("Excited", "Excited 🤩"),
    ("Tired", "Tired 😴"),
    ("Grateful", "Grateful 🙏"),
    ("Other", "Other ✍️"),
]



class MoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=100, choices=MOOD_CHOICES)
    intensity = models.CharField(max_length=100, choices=INTENSITY_LEVEL)
    journal_text = models.TextField(max_length=250)
    affirmation = models.TextField(blank=True, null=True)
    created_at = models.DateField("Journal Date", default=datetime.date.today)

    def __str__(self):
        return f"{self.mood} ({self.id})"

    def get_absolute_url(self):
        return reverse("mood-detail", kwargs={"pk": self.pk})

```







```python

INSTALLED_APPS = [
    "main_app",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

```


```python
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

class Home(LoginView):
    template_name = "home.html"

class MoodCreate(CreateView):
    model = MoodEntry
    fields = ['mood', 'intensity', 'journal_text']
    
    def form_valid(self, form):
        form.instance.user = self.request.user

        mood = form.cleaned_data['mood']
        journal_text = form.cleaned_data['journal_text']
        api_key = os.getenv("GEMINI_API_KEY")

        affirmation = generate_affirmation(api_key, mood, journal_text)
        
        form.instance.affirmation = affirmation

        return super().form_valid(form)

def moods_index(request):
    moods = MoodEntry.objects.filter(user=request.user).order_by('-created_at')
    
    mood_summary = (
        MoodEntry.objects
        .filter(user=request.user)
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


def mood_detail(request, pk):
    mood = MoodEntry.objects.get(id=pk)
    affirmation = request.session.pop('affirmation', None)
    return render(request, 'moods/detail.html', {
        'mood': mood,
        'affirmation': affirmation
    })


