from django.contrib import admin
from django.urls import path

from .views import rate_index, update_rate_data

urlpatterns = [
    path("rate/", rate_index, name="rateDataUrlName"),
    path("rate/update-db", update_rate_data, name="rateDataUpdateUrlName"),
]
