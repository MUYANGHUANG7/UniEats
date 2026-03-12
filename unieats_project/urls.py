from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reviews_app.urls')),
]

# Deployment note: when running behind a WSGI server without a dedicated static file server,
# serving static assets via Django prevents MIME-type issues (e.g., CSS returning HTML).
urlpatterns += staticfiles_urlpatterns()
