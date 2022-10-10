"""traveldiary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path
from map.views import SignUpView, add_marker, show_markers_on_map, HomeView, update_profile, make_photo_gallery, delete_marker, \
    manage_markers, update_marker, delete_photo
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),

    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('password_change/', PasswordChangeView.as_view(template_name='accounts/change_password.html'), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='accounts/change_password_done.html'), name='password_change_done'),
    path('profile/', update_profile, name='profile'),

    path('add_marker/', add_marker, name='add_marker'),
    path('map/', show_markers_on_map, name='map'),
    path('update_marker/<pk>/', update_marker, name='update_marker'),
    path('delete_marker/<pk>/', delete_marker, name='delete_marker'),
    path('markers_manager/', manage_markers, name='manage_markers'),

    path('photo_gallery/', make_photo_gallery, name='photo_gallery'),
    path('delete_photo/<pk>/', delete_photo, name='delete_photo'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
