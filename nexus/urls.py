"""
URL configuration for nexus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('events/', include('events.urls')),  # events app URLs
    path('api/', include('api.urls')), # API urls
    path('chat/', include('chat.urls', namespace='chat')), # chat urls
 
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    #had to delete a url because i got the namespace error
    # path('accounts/', include('accounts.urls')),  # Ensure namespace is set
    # path('accounts/', include('accounts.urls', namespace='accounts')),  # Ensure namespace is set

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
