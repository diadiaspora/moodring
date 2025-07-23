from django.urls import path
from . import views  # Import views to connect routes to view functions

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("about/", views.about, name="about"),
    # DELETE THIS LINE ENTIRELY:
    # path("accounts/signup/", views.signup, name="signup"),
    path('moods/', views.moods_index, name='moods'),
    path('moods/create/', views.MoodCreate.as_view(), name='mood-create'),
    path('moods/<int:pk>/', views.mood_detail, name='mood-detail'),
    path('moods/<int:pk>/update/', views.MoodUpdate.as_view(), name='mood-update'),
    path('moods/<int:pk>/delete/', views.MoodDelete.as_view(), name='mood-delete'),
]



