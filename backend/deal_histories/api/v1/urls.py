"""URLs configuration of the 'api' application v1."""

from django.urls import path

from api.v1.views import (
    FileUploadView,
    # FileDetailsView,
    TopSpendingCustomerView,
)

urlpatterns = [
    path("upload-csv-file/", FileUploadView.as_view(), name="upload-csv-file"),
    path(
        "top-customers/<int:id>/",
        TopSpendingCustomerView.as_view(),
        name="top-customers",
    ),
    # path("file_detail/<int:id>/", FileDetailsView.as_view(), name="file_detail"),
]
