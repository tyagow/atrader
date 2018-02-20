from django.conf.urls import url
from src.core.views import HomeView


app_name = 'Core'



urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
]
