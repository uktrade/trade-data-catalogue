from django.contrib import admin
from django.urls import path

from dataset_catalogue.views import (
    DatasetCatalogueView,
    DatasetDetailsView,
    DatasetDataPreviewView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        DatasetCatalogueView.as_view(),
        name="dataset_catalogue_view",
    ),
    path(
        "dataset-id-<str:dataset_id>/<str:version>",
        DatasetDetailsView.as_view(),
        name="dataset_details_view",
    ),
    path(
        "dataset-id-<str:dataset_id>/<str:version>/<str:data_type>/<str:data_id>",
        DatasetDataPreviewView.as_view(),
        name="dataset_data_preview_view",
    ),
]
