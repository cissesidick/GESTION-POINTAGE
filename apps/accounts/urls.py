from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .auth_views import CustomLoginView

app_name = 'accounts'

urlpatterns = [
    path('login/',  CustomLoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/auth/login/'),           name='logout'),
    path('init/',   views.initialiser_compte,                                         name='init'),
]
