import base64
import folium
import geocoder
from PIL import Image
from cloudinary import CloudinaryImage, uploader
from folium import IFrame
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from map.forms import SignUpForm, AddMarkerForm, ProfileForm, UserForm, AddPhotoForm, UpdateMarkerForm
from django.contrib.auth.decorators import login_required
from .models import Marker, Photo


class HomeView(TemplateView):
    template_name = 'home.html'


class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')


@login_required()
def update_profile(request):
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
def add_marker(request):
    if request.method == 'POST':
        form = AddMarkerForm(request.POST)
        photo_form = AddPhotoForm(request.FILES)
        location = request.POST['location']
        g = geocoder.osm(location)
        if not g.ok:
            messages.error(request, 'Invalid location.')
        if form.is_valid() and g.ok:
            marker = form.save(commit=False)
            marker.user = request.user
            marker.lat = g.lat
            marker.lng = g.lng
            marker.save()

            photos = request.FILES.getlist('photo')
            for photo in photos:
                Photo.objects.create(photo=photo, marker=Marker.objects.last(), user_id=request.user.id)

            messages.success(request, 'Marker has been added successfully.')
            return redirect('map')

    else:
        form = AddMarkerForm()
        photo_form = AddPhotoForm()

    m = folium.Map(location=[0, 0], zoom_start=1, min_zoom=1, max_bounds=True)
    m = m._repr_html_()
    context = {'m': m, 'form': form, 'photo_form': photo_form}
    return render(request, 'map/add_marker.html', context)


@login_required()
def show_markers_on_map(request):
    m = folium.Map(location=[10, 0], height='100%', zoom_start=2, min_zoom=1, max_bounds=True)
    current_user = request.user.id
    markers = Marker.objects.all().filter(user_id=current_user)
    for marker in markers:
        lat = marker.lat
        lng = marker.lng
        location = marker.location
        date = marker.date
        desc = marker.description
        photos = Photo.objects.all().filter(marker_id=marker.id)

        html = f'<div id="title">{location}</div><div id="desc">{desc}</div><div id="date">{date}</div>'
        if photos:
            photo = photos.last().photo
            photo_name = str(photo).split('/')[-1]
            html_photo = CloudinaryImage(photo_name).image(width=190, crop='scale')
            html += html_photo
            iframe = IFrame(html, width=200, height=220)
        else:
            iframe = IFrame(html, width=150, height=70)

        popup = folium.Popup(iframe)
        folium.Marker([lat, lng], popup=popup).add_to(m)

    m = m._repr_html_()
    context = {'m': m}
    return render(request, 'map/map_view.html', context)


@login_required()
def update_marker(request, pk):
    marker = Marker.objects.get(id=pk)
    photos = Photo.objects.filter(marker_id=marker.id)
    if request.method == 'POST':
        photos = request.FILES.getlist('photo')
        for photo in photos:
            Photo.objects.create(photo=photo, marker_id=marker.id, user_id=request.user.id)

        form = UpdateMarkerForm(request.POST, instance=marker)
        if form.is_valid():
            form.save()

            messages.success(request, 'Your travel memory has been updated successfully.')
            return redirect('update_marker', pk=marker.id)

    form = AddMarkerForm(instance=marker)
    photo_form = AddPhotoForm()

    context = {'form': form,  'photo_form': photo_form, 'marker': marker, 'photos': photos}
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
def make_photo_gallery(request):
    current_user = request.user.id
    photos = Photo.objects.filter(user_id=current_user)
    context = {'photos': photos}

    return render(request, 'photo_gallery.html', context)


@login_required()
def delete_photo(request, pk):
    photo = Photo.objects.get(id=pk)
    if request.method == 'POST':
        photo.delete()
        messages.success(request, 'Photo has been deleted')
        return redirect('manage_markers')

    context = {'photo': photo}
    return render(request, 'photo_confirm_delete.html', context)


def resize_photo(photo):
    new = CloudinaryImage(photo).image(height=300, width=50)

    return new