from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('API/v1/', include('event.urls')),
    
                  path('rest-auth/', include('dj_rest_auth.urls')),
                  path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),
                
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
