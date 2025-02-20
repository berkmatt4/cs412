#urls.py provides the url paths for the mini_fb app

from django.urls import path
from django.conf import settings
from .views import ShowAllProfilesView, ShowProfilePageView

#defining only two - default link to show_all_profiles
#another to show a single profile details
urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile")
]