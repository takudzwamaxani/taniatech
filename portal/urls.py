from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    # Project URLs
    path('', views.index, name='index'),
    path('jobs', views.jobs, name='jobs'),
    path("news/<slug:slug>/", views.news_detail, name="news_detail"),
    path("job/<int:id>/", views.job_detail, name="job_detail"),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('faq', views.faq, name='faq'),
    path('plan', views.faq, name='plan'),
    path('tos', views.tos, name='tos'),
    path('policy', views.privacy, name='policy'),
    path('guide', views.guide, name='guide'),
    path('chat', views.chat, name='chat'),
    path('login', views.login, name='login'),
    path('forgot', views.password_reset_request, name='forgot'),
    path('logout', views.logout, name='logout'),
    path('register', views.signup, name='register'),
    path('news', views.news, name='news'),
    path('team', views.team, name='team'),
    path('cvs', views.cvprofile_manage, name='cvs'),
    path('scenter', views.support_center, name='scenter'),
    path('plans', views.plans, name='plans'),
    path('sitemap', views.sitemap, name='sitemap'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)