from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.urls import re_path

urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('accounts/login/',
         LoginView.as_view(template_name='chat_channel/login.html'), name='login'),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
