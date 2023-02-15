import base64
import folium
import geocoder
from folium import IFrame
from PIL import Image
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, UpdateView
from .forms import SignUpForm, AddMarkerForm, ProfileForm, UserForm, AddPhotoForm, UpdateMarkerForm
from .models import Marker, Photo


class HomeView(TemplateView):
    template_name = 'map/home.html'


class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')


@login_required()
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile has been updated successfully.')
            return redirect(to='profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)

    return render(request, 'accounts/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required()
def display_map_with_markers(request):
    m = folium.Map(location=[10, 0], height='75%', zoom_start=2, min_zoom=2, max_bounds=True)
    user = request.user
    markers = Marker.objects.filter(user_id=user)
    for marker in markers:
        lat = marker.lat
        lng = marker.lng
        location = marker.location
        date = marker.date
        desc = marker.description
        photos = Photo.objects.filter(marker=marker)

        html = f'<div id="title">{location}</div><div id="desc">{desc}</div><div id="date">{date}</div>'
        if photos:
            photo = photos.last().photo
            smaller_photo = resize_photo(photo)
            encoded = base64.b64encode(open(smaller_photo, 'rb').read()).decode('UTF-8')
            html_photo = f'<img src="data:image/png;base64,{encoded}">'
            html += html_photo
            iframe = IFrame(html, width=180, height=250)
        else:
            iframe = IFrame(html, width=160, height=60)

        popup = folium.Popup(iframe)
        folium.Marker([lat, lng], popup=popup).add_to(m)

    m = m._repr_html_()
    context = {'m': m}
    return render(request, 'map/map_view.html', context)


@login_required()
def add_marker(request):
    if request.method == 'POST':
        marker_form = AddMarkerForm(request.POST)
        photo_form = AddPhotoForm(request.POST, request.FILES)
        photos = request.FILES.getlist('photo')

        location = request.POST['location']
        g = geocoder.osm(location)
        if not g.ok:
            messages.error(request, 'Invalid location.')

        if marker_form.is_valid() and g.ok and photo_form.is_valid():
            location = marker_form.cleaned_data['location']
            date = marker_form.cleaned_data['date']
            description = marker_form.cleaned_data['description']
            lat = g.lat
            lng = g.lng
            user = request.user
            marker_instance = Marker.objects.create(
                location=location,
                date=date,
                description=description,
                lat=lat,
                lng=lng,
                user=user
            )

            for photo in photos:
                Photo.objects.create(user=user, marker=marker_instance, photo=photo)

            messages.success(request, 'Marker has been added successfully.')
            return redirect('map')

    else:
        form = AddMarkerForm()
        photo_form = AddPhotoForm()

    m = folium.Map(location=[0, 0], zoom_start=2, min_zoom=2, max_bounds=True)
    m = m._repr_html_()
    context = {'m': m, 'form': form, 'photo_form': photo_form}
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
def create_photo_gallery(request):
    current_user = request.user.id
    photos = Photo.objects.filter(user_id=current_user)
    context = {'photos': photos}
    return render(request, 'map/photo_gallery.html', context)


def add_photo(request, pk):
    marker = Marker.objects.get(id=pk)
    if request.method == 'POST':
        photo_form = AddPhotoForm(request.POST, request.FILES)
        photos = request.FILES.getlist('photo')
        if photo_form.is_valid():
            for photo in photos:
                user = request.user
                Photo.objects.create(photo=photo, marker=marker, user=user)
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


def resize_photo(photo):
    path = photo.path
    photo = Image.open(path)
    result_width = 150
    width_percent = (result_width / float(photo.size[0]))
    hsize = int((float(photo.size[1]) * float(width_percent)))
    smaller_photo = photo.resize((result_width, hsize), Image.ANTIALIAS)
    smaller_photo_path = f'{path} + resized.jpg'
    smaller_photo.save(smaller_photo_path, 'JPEG', quality=100)
    return smaller_photo_path
