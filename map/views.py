from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from map.forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .forms import UpdateProfileForm, UpdateUserForm
from .signals import create_profile
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
        profile_form=UpdateProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html',{'user_form':user_form, 'profile_form':profile_form})




