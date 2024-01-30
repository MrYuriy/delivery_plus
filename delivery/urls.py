from django.urls import path, include
from .views import (
    SelectReceptionView,
    DeliveryCreateView,
    DeleveryDetailView, 
    HomeView, DeliveryStorageView,

    )

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("reception/", SelectReceptionView.as_view(), name="select_receprion"),
    path("reception/create/", DeliveryCreateView.as_view(), name="delivery_create"),
    path("storage/", DeliveryStorageView.as_view(), name="delivery_storage"),
    path("<int:pk>/detail/", DeleveryDetailView.as_view(), name="delivery_detail")
]
app_name = "delivery"