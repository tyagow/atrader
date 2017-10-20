from django.conf.urls import url

from src.core.views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
]
