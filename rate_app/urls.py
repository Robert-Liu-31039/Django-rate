from django.contrib import admin
from django.urls import path

from .views import rate_index, update_rate_data

urlpatterns = [
    path("", rate_index, name="rateDataUrlName"),
    path("update-db", update_rate_data, name="rateDataUpdateUrlName"),
]
