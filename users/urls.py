from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path
from .views import SignUpView, profile


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password_change/', PasswordChangeView.as_view(template_name='users/change_password.html'), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='users/change_password_done.html'), name='password_change_done'),
    path('profile/', profile, name='profile'),
]
