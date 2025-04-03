#storing url patterns for site navigation

from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.VoterListView.as_view(), name = 'home'),
    path(r'voters', views.VoterListView.as_view(), name = 'voter_list'),
    path(r'voter/<int:pk>', views.VoterDetailView.as_view(), name = 'voter_details'),
    path(r'graphs', views.GraphListView.as_view(), name = 'graphs'),
    

]