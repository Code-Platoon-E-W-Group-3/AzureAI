from django.urls import path
from .views import analyze_resume, chat_resume_analysis


urlpatterns = [
    path('resume-analyze/', analyze_resume, name='analyze-resume'),
    path('chat-resume/', chat_resume_analysis, name='chat-resume'),
]

