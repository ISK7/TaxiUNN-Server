from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('clients/auth/', include('client_auth.urls')),
    path('admins/auth/', include('admin_auth.urls')),
]
