from django.contrib import messages

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from map.forms import SignUpForm


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



