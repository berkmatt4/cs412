from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    #URLs defined for the quotes project
   path(r'', views.quote_page, name = "quote_page"),
   path(r'quote', views.quote_page, name="quote_page"),
   path(r'show_all', views.all_page, name="all_page"),
   path(r'about',views.about_page, name="about_page"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)