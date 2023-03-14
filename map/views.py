import base64
import folium
import geocoder
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from folium import IFrame
from PIL import Image
from .forms import AddMarkerForm, AddPhotoForm, UpdateMarkerForm
from .models import Marker, Photo


class HomeView(TemplateView):
    template_name = 'map/home.html'


@login_required()
def display_map_with_markers(request):
    folium_map = folium.Map(location=[10, 0], height='75%', zoom_start=2, min_zoom=2, max_bounds=True)
    markers = Marker.objects.filter(user=request.user).all()
    photos = Photo.objects.filter(user=request.user).all()
    for marker in markers:
        iframe = create_iframe(marker, photos)
        popup = folium.Popup(iframe)
        folium.Marker([marker.lat, marker.lng], popup=popup).add_to(folium_map)

    folium_map = folium_map._repr_html_()
    context = {'folium_map': folium_map}
    return render(request, 'map/map_view.html', context)


@login_required()
def add_marker(request):
    if request.method == 'POST':
        marker_form = AddMarkerForm(request.POST)
        photo_form = AddPhotoForm(request.POST, request.FILES)
        photos = request.FILES.getlist('photo')
        geolocator = geocoder.osm(request.POST['location'])
        if not geolocator.ok:
            messages.error(request, 'Invalid location.')

        if marker_form.is_valid() and geolocator.ok and photo_form.is_valid():
            location = marker_form.cleaned_data['location']
            date = marker_form.cleaned_data['date']
            description = marker_form.cleaned_data['description']
            lat = geolocator.lat
            lng = geolocator.lng
            user = request.user
            marker = Marker.objects.create(
                location=location,
                date=date,
                description=description,
                lat=lat,
                lng=lng,
                user=user
            )
            for photo in photos:
                Photo.objects.create(user=user, marker=marker, photo=photo)

            messages.success(request, 'Marker has been added successfully.')
            return redirect('map')

    form = AddMarkerForm()
    photo_form = AddPhotoForm()

    folium_map = folium.Map(location=[0, 0], zoom_start=2, min_zoom=2, max_bounds=True)
    folium_map = folium_map._repr_html_()
    context = {'folium_map': folium_map, 'form': form, 'photo_form': photo_form}
    return render(request, 'map/add_marker.html', context)


@login_required()
def update_marker(request, pk):
    marker = Marker.objects.get(id=pk)
    photos = Photo.objects.filter(marker=marker)
    if request.method == 'POST':
        marker_form = UpdateMarkerForm(request.POST, instance=marker)
        if marker_form.is_valid():
            marker_form.save()
            messages.success(request, 'Your travel memory has been updated successfully.')
            return redirect('update_marker', pk=marker.id)

    form = AddMarkerForm(instance=marker)
    context = {'form': form, 'marker': marker, 'photos': photos}
    return render(request, 'map/update_marker.html', context)


@login_required()
def delete_marker(request, pk):
    marker = Marker.objects.get(id=pk)
    if request.method == 'POST':
        marker.delete()
        messages.success(request, 'Marker has been deleted')
        return redirect('manage_markers')

    context = {'marker': marker}
    return render(request, 'map/marker_confirm_delete.html', context)


@login_required()
def manage_markers(request):
    markers = Marker.objects.filter(user=request.user)
    context = {'markers': markers}
    return render(request, 'map/marker_manager.html', context)


@login_required()
def display_photo_gallery(request):
    photos = Photo.objects.filter(user=request.user).select_related('marker').all()
    context = {'photos': photos}
    return render(request, 'map/photo_gallery.html', context)


@login_required()
def add_photo(request, pk):
    marker = Marker.objects.get(id=pk)
    if request.method == 'POST':
        photo_form = AddPhotoForm(request.POST, request.FILES)
        photos = request.FILES.getlist('photo')
        if photo_form.is_valid():
            for photo in photos:
                Photo.objects.create(photo=photo, marker=marker, user=request.user)
            messages.success(request, 'Photo has been added successfully.')
            return redirect('update_marker', pk=marker.id)

    photo_form = AddPhotoForm()
    context = {'photo_form': photo_form, 'marker': marker}
    return render(request, 'map/add_photo.html', context)


@login_required()
def delete_photo(request, pk):
    photo = Photo.objects.get(id=pk)
    if request.method == 'POST':
        photo.delete()
        messages.success(request, 'Photo has been deleted')
        return redirect('manage_markers')

    context = {'photo': photo}
    return render(request, 'map/photo_confirm_delete.html', context)


def create_iframe(marker, photos):
    popup_content = f'{marker.location}<br>{marker.date}<br>{marker.description}'
    try:
        photo = photos.filter(marker=marker).last()
        resized_photo = resize_photo(photo.photo)
        encoded_photo = encode_photo(resized_photo)
        popup_photo = f'<img src="data:image/jpg;base64,{encoded_photo}">'
        popup_content += popup_photo
        iframe = IFrame(popup_content, width=180, height=300)
    except AttributeError:
        iframe = IFrame(popup_content, width=180, height=50)

    return iframe


def resize_photo(photo):
    path = photo.path
    photo = Image.open(path)
    result_width = 150
    width_percent = (result_width / float(photo.size[0]))
    hsize = int((float(photo.size[1]) * float(width_percent)))
    resized_photo = photo.resize((result_width, hsize), Image.ANTIALIAS)
    resized_photo_path = f'{path}resized.jpg'
    resized_photo.save(resized_photo_path, 'JPEG', quality=100)
    return resized_photo_path


def encode_photo(photo):
    with open(photo, 'rb') as photo_file:
        encoded_string = base64.b64encode(photo_file.read()).decode('UTF-8')
        return encoded_string
