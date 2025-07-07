from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.contrib.auth import views as auth_views
# admin.site.__class__ = OTPAdminSite 
admin.site.site_header = "TaniaTech Portal"
admin.site.site_title = "TaniaTech Portal"
admin.site.index_title = "Welcome to TaniaTech Portal Administration"

# Language switch
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(  # ✅ No string as first tuple item
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),
    # path('zaha/', include('cms.urls')),
)

# Static/media in dev
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
