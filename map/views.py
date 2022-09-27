import base64
from django.urls import reverse_lazy
from folium import IFrame
import folium
import geocoder
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from map.forms import SignUpForm, AddMarkerForm, ProfileForm, UserForm
from django.contrib.auth.decorators import login_required
from .models import Location

class HomeView(TemplateView):
    template_name = 'accounts/home.html'


class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    #
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data.get('username')
    #         messages.success(request, f'Account created for {username}')
    #
    #         return redirect(to='login')
    #
    #     return render(request, self.template_name, {'form': form})


@login_required()
def create_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile was updated successfully')
            return redirect(to='profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

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
                return render(request, 'add_marker.html')
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
    return render(request, 'add_marker.html', context)


@login_required()
def show_locations(request):
    current_user = request.user.id
    m = folium.Map(location=[10, 0], height='75%', zoom_start=2, min_zoom=2, max_bounds=True)
    markers = Location.objects.all().filter(user_id=current_user)
    for marker in markers:
        lat = marker.lat
        lng = marker.lng
        city = marker.name
        date = marker.date
        desc = marker.description

        encoded = base64.b64encode(open(marker.photo.path, 'rb').read()).decode('UTF-8')
        html = f'<div id="title">{city}</div><div id="date">{desc}</div><div id="date">{date}</div><img src="data:image/png;base64,{encoded}">'
        iframe = IFrame(html, width=200, height=200)
        popup = folium.Popup(iframe)
        folium.Marker([lat, lng], popup=popup).add_to(m)

    m = m._repr_html_()
    context = {'m': m}
    return render(request, 'map_view.html', context)
