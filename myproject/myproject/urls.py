from django.contrib import admin
from django.urls import include, path, re_path

from myproject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
