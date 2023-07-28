"""URLs configuration of the 'api' application v1."""

from django.urls import path

from api.v1.views import FileUploadView, TopSpendingCustomerView

urlpatterns = [
    path("upload-csv-file/", FileUploadView.as_view(), name="upload-csv-file"),
    path(
        "top-customers/",
        TopSpendingCustomerView.as_view(),
        name="top-customers",
    ),
]
