
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


from django.urls import path, include

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html')),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('catalog.urls')),
    path('', include('cart.urls')),
    path('', include('orders.urls')),
    path('', include('reviews.urls')),


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
