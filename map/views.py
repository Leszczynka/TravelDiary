import base64

from folium import IFrame
import folium
import geocoder
from django.contrib import messages
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
    m = folium.Map(location=[0, 0], zoom_start=2, min_zoom=2, max_bounds=True)
    if request.method == 'POST':
        form = AddMarkerForm(request.POST, request.FILES)
        if form.is_valid():
            location = form.cleaned_data['name']
            g = geocoder.osm(location)
            if not g.ok:
                messages.error(request, "Invalid location")
                return render(request, 'map.html')
            lat = g.lat
            lng = g.lng

            Location.objects.create(name=location,
                                    date=form.cleaned_data['date'],
                                    description=form.cleaned_data['description'],
                                    photo=form.cleaned_data['photo'],
                                    lat=lat,
                                    lng=lng,
                                    user_id=request.user.id)
        return redirect('map')
    else:
        form = AddMarkerForm()

    m = m._repr_html_()
    context = {'m': m, 'form': form}
    return render(request, 'map.html', context)


@login_required()
def show_locations(request):
    current_user = request.user.id
    m = folium.Map(location=[10, 0], zoom_start=2, min_zoom=2, max_bounds=True)
    markers = Location.objects.all().filter(user_id=current_user)
    for marker in markers:
        lat = marker.lat
        lng = marker.lng
        encoded = base64.b64encode(open(marker.photo.path, 'rb').read())
        html = '<img src="data:image/png;base64,{}">'.format
        iframe = IFrame(html(encoded.decode('UTF-8')), width=300, height=300)

        popup = folium.Popup(iframe)
        folium.Marker([lat, lng], popup=popup).add_to(m)

    m = m._repr_html_()
    context = {'m': m}
    return render(request, 'map_with_markers.html', context)
