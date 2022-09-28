import base64
import folium
import geocoder
from django.urls import reverse_lazy
from folium import IFrame
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from map.forms import SignUpForm, AddMarkerForm, ProfileForm, UserForm
from django.contrib.auth.decorators import login_required
from .models import Marker


class HomeView(TemplateView):
    template_name = 'accounts/home.html'


class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')


@login_required()
def create_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile was updated successfully')
            return redirect(to='profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)

    return render(request, 'accounts/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required()
def add_marker(request):
    m = folium.Map(location=[0, 0], zoom_start=2, min_zoom=2, max_bounds=True)
    if request.method == 'POST':
        form = AddMarkerForm(request.POST, request.FILES)
        if form.is_valid():
            location = form.cleaned_data['location']
            g = geocoder.osm(location)
            if not g.ok:
                messages.error(request, "Invalid location")
                return redirect(to='add_marker')

            lat = g.lat
            lng = g.lng
            Marker.objects.create(location=location,
                                  date=form.cleaned_data['date'],
                                  description=form.cleaned_data['description'],
                                  photo=form.cleaned_data['photo'],
                                  lat=lat,
                                  lng=lng,
                                  user_id=request.user.id)
            messages.success(request, "Marker added succesfully!")
        return redirect('map')
    else:
        form = AddMarkerForm()

    m = m._repr_html_()
    context = {'m': m, 'form': form}
    return render(request, 'add_marker.html', context)


@login_required()
def show_map(request):
    current_user = request.user.id
    m = folium.Map(location=[10, 0], height='75%', zoom_start=2, min_zoom=2, max_bounds=True)
    markers = Marker.objects.all().filter(user_id=current_user)
    for marker in markers:
        lat = marker.lat
        lng = marker.lng
        city = marker.location
        date = marker.date
        desc = marker.description
        photo = marker.photo

        if photo:
            encoded = base64.b64encode(open(marker.photo.path, 'rb').read()).decode('UTF-8')
            html = f'<div id="title">{city}</div><hr><div id="desc">{desc}</div><hr><div id="date">{date}</div><br><img src="data:image/png;base64,{encoded}">'
            iframe = IFrame(html, width=230, height=260)
        else:
            html = f'<div id="title">{city}</div><hr><div id="desc">{desc}</div><hr><div id="date">{date}</div>'
            iframe = IFrame(html, width=130, height=130)
        popup = folium.Popup(iframe)
        folium.Marker([lat, lng], popup=popup).add_to(m)

    m = m._repr_html_()
    context = {'m': m}
    return render(request, 'map_view.html', context)


def make_photo_gallery(request):
    current_user = request.user.id
    user_data = Marker.objects.all().filter(user_id=current_user)
    context = {'user_data': user_data}

    return render(request, 'photo_gallery.html', context)