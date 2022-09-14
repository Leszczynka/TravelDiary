import folium
import geocoder
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from map.forms import SignUpForm, AddMarkerForm
from django.contrib.auth.decorators import login_required
from .forms import UpdateProfileForm, UpdateUserForm
from .models import Location


def home(request):
    return render(request, 'accounts/home.html')


class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


@login_required()
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile was updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required()
def add_location(request):
    location = request.POST.get('name')
    g = geocoder.osm(location)
    lat = g.lat
    lng = g.lng
    if request.method == 'POST':
        form = AddMarkerForm(request.POST)
        if form.is_valid():
            Location.objects.create(
                name=location,
                lat=lat,
                lng=lng,
                user_id=request.user.id
            )
        return redirect('map')
    else:
        form = AddMarkerForm()

    location = Location.objects.all().last()
    lat = location.lat
    lng = location.lng
    m = folium.Map(location=[52.237049, 21.017532], zoom_start=2)
    if isinstance(lat, float) and isinstance(lng, float):
        folium.Marker([lat, lng]).add_to(m)
    else:
        messages.error(request, "Invalid location")

    m = m._repr_html_()
    context = {'m': m, 'form': form}
    return render(request, 'map.html', context)


def show_locations(request):
    current_user = request.user.id
    m = folium.Map(location=[52.237049, 21.017532], zoom_start=2)
    markers = Location.objects.all().filter(user_id=current_user)
    for marker in markers:
        lat = marker.lat
        lng = marker.lng
        folium.Marker([lat, lng]).add_to(m)

    m = m._repr_html_()
    context = {'m': m}
    return render(request, 'map_with_markers.html', context)
