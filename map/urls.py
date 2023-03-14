from django.urls import path
from .views import add_marker, display_map_with_markers, HomeView, display_photo_gallery, delete_marker, manage_markers, update_marker, delete_photo, add_photo

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('map/', display_map_with_markers, name='map'),
    path('add_marker/', add_marker, name='add_marker'),
    path('update_marker/<pk>/', update_marker, name='update_marker'),
    path('delete_marker/<pk>/', delete_marker, name='delete_marker'),
    path('manage_markers/', manage_markers, name='manage_markers'),
    path('photo_gallery/', display_photo_gallery, name='photo_gallery'),
    path('add_photo/<pk>/', add_photo, name='add_photo'),
    path('delete_photo/<pk>/', delete_photo, name='delete_photo'),
]