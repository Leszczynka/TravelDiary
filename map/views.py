from django.contrib import messages
from django.contrib.gis.admin import OSMGeoAdmin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView
import folium
import geocoder
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from traveldiary import settings
from .forms import UpdateProfileForm, UpdateUserForm, SearchForm, SignUpForm
from .models import LocationMarker, Location


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

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})


@login_required()
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {'user_form': user_form, 'profile_form': profile_form})



@login_required()
def mapviev(request):
    form = SearchForm(request.POST)
    addres = request.POST.get('address')
    g = geocoder.osm(addres)
    lat = g.lat
    lng = g.lng
    # if g.ok is False:
    if request.method == 'POST':
        if form.is_valid():
            Location.objects.create(address=addres,lat=lat,lng=lng,user_id=request.user.id)
            return redirect('map')
    else:
        form = SearchForm()
    m = folium.Map(location=[50.9025547, 18.93716], zoom_start=10, max_zoom=12)
    try:
        folium.Marker([lat, lng],
                  tooltip='Click for more').add_to(m)
    except ValueError:
        pass
    # Get HTML Representation of Map Object
    m = m._repr_html_()
    context = {
        'm': m,
        'form': form,
    }
    return render(request, 'map.html', context)

