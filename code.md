




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
```




```html
<body style="margin: 0; padding: 0; overflow-y: auto;">
  <header
    style="position: static; height: 80px; width: 100%; padding-left: 21px; padding-right: 21px; background-color: transparent;">
    <div class="header-logo-container" style="border-radius: 7px; background-color: #ffffff; width: 180px;">
      <a href="{% url 'home' %}" style="text-decoration: none;">
        <div style="display: flex;">
          <img src="{% static 'images/header1.png' %}" class="header-ring" alt="Logo"
            style="width: 18%; margin-top: -2px; margin-left: 0px; margin-right: 60px;" />
          <h3 style="font-size: 16px; text-decoration: none; color: #000000; margin-top: 0px; margin-left: -50px;">Mood
            Ring</h3>
        </div>
      </a>
    </div>
    <nav style="border-radius: 7px; background-color: #ffffff;">
      <ul>
        <li><a href="{% url 'moods' %}" style="color: #000000;">Dashboard</a></li>
        <li><a href="{% url 'mood-create' %}" style="color: #000000;">Log a Mood</a></li>
        <li><a href="{% url 'about' %}" style="color: #000000;">Resources</a></li>
       
      </ul>
    </nav>
  </header>

  <main>
    {% block content %}
    <div style="display: flex; justify-content: flex-end;">
      <button type="submit" style="
            margin-right: 40px;
            padding: 10px 18px;
            background-color: #f1d6b8;
            color: #000000;
            font-weight: bold;
            border: 2px solid #000000;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            margin-top: 12px;
            font-size: 14px;
         
          " onmouseover="this.style.backgroundColor='#e2c099';" onmouseout="this.style.backgroundColor='#f1d6b8';">
        Submit!
      </button>
    </div>
    {% endblock %}
  </main>
</body>
```

```python
{% extends 'base.html' %}
{% load static %}

{% block head %}
<link rel="stylesheet" href="{% static 'css/resources.css' %}" />
{% endblock %}

{% block content %}
<section class="page-header">
  <h1 style="color: #000000;">Mental Health Resources</h1>
  <p style="color: #000000; font-size: 16px; width: 600px; text-align: justify; margin-left: auto; margin-right: auto;">
    Taking care of your mind is just as important as caring for your body. Below are trusted resources you can explore
    for support, learning, or just someone to talk to.</p>
</section>

<section class="resources-list" >
  <article class="resource-card" style="background-color: white;>
    <h2 style="color: #000000;">National Suicide Prevention Lifeline</h2>
    <p style="color: #000000; "><strong>Call or Text:</strong> <a href="tel:988">988</a></p>
    <p style="color: #000000; font-size: 14px;">Free and confidential support 24/7 for people in distress, prevention and crisis resources.</p>
    <a href="https://988lifeline.org" target="_blank">Visit Website</a>
  </article>

  <article class="resource-card" style="background-color: white;>
    <h2 style="color: #000000;">Crisis Text Line</h2>
    <p style="color: #000000;"><strong>Text:</strong> HOME to 741741</p>
    <p style="color: #000000; font-size: 14px;">24/7 support from trained crisis counselors, via text message.</p>
    <a href="https://www.crisistextline.org" target="_blank">Visit Website</a>
  </article>

  <article class="resource-card" style="background-color: white;>
    <h2 style="color: #000000;">Therapy Matcher</h2>
    <p style="color: #000000; font-size: 14px;">Find mental health professionals near you or online that fit your needs.</p>
    <a href="https://www.psychologytoday.com" target="_blank">Find a Therapist</a>
  </article>

  <article class="resource-card" style="background-color: white;">
    <h2 style="color: #000000;">NAMI (National Alliance on Mental Illness)</h2>
    <p style="color: #000000; font-size: 14px;">Educational resources, peer support, and mental health advocacy.</p>
    <a href="https://www.nami.org/Home" target="_blank">Visit NAMI</a>
  </article>
</section>
{% endblock %}

```

```python


<!-- Mood Cards -->
<section class="card-container">
  {% for mood in moods %}
  <a href="{% url 'mood-detail' mood.id %}" class="card-link" style="text-decoration: none;">
    <div class="card" style="background-color: #ffffff;">
      <div class="card-content">
        <div class="card-img-container">
          <img src="{% static 'images/header1.png' %}" alt="Mood Icon" />
        </div>
        <h2 class="card-title" style="color: #000000;  font-size: 16px;">{{ mood.created_at }}</h2>
      </div>
    </div>
  </a>
  {% endfor %}
</section>

<!-- Chart JS Script -->
<script>
  document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('moodChart').getContext('2d');
    const moodChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: {{ mood_labels| safe }},
    datasets: [{
      label: 'Mood Count',
      data: {{ mood_data| safe }},
    backgroundColor: {{ mood_colors| safe }},
    borderWidth: 1
        }]
      },
    options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'right',
        labels: {
          boxWidth: 20,
          padding: 15
        }
      },
      tooltip: {
        enabled: true
      }
    },
    layout: {
      padding: 10
    }
  }
    });
  });
</script>
{% endblock %}


```