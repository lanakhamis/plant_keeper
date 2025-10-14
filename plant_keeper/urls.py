"""
URL configuration for planet_keeper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.conf import settings  # 💡 أضيفي هذا
from django.conf.urls.static import static  # 💡 أضيفي هذا


urlpatterns = [
    path("admin/", admin.site.urls),
    # هذا يربط روابط main_app
    path("", include("main_app.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("plants/", include("main_app.urls")),  #
#     path(
#         "",
#         auth_views.LoginView.as_view(template_name="plants/login.html"),
#         name="login",
#     ),  # هنا
#     path("signup/", include("main_app.urls")),  # لو عندك signup هنا
# ]


# # 💡 أضيفي هذا الجزء ليعمل تحميل الصور
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
