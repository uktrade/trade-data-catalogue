from django.contrib import admin
from django.urls import path

from dataset_catalogue.views import DatasetCatalogueView, DatasetDetailsView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        DatasetCatalogueView.as_view(),
        name="dataset_catalogue_view",
    ),
    path(
        "<str:dataset_id>/<str:version>",
        DatasetDetailsView.as_view(),
        name="dataset_details_view",
    ),
]
