from django.db import models
from django.urls import reverse
import datetime

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
    # The 'user' ForeignKey line should be gone completely from here.
    mood = models.CharField(max_length=100, choices=MOOD_CHOICES)
    intensity = models.CharField(max_length=100, choices=INTENSITY_LEVEL)
    journal_text = models.TextField(max_length=250)
    affirmation = models.TextField(blank=True, null=True)
    created_at = models.DateField("Journal Date", default=datetime.date.today)

    def __str__(self):
        return f"{self.mood} ({self.id})"

    def get_absolute_url(self):
        return reverse("mood-detail", kwargs={"pk": self.pk})