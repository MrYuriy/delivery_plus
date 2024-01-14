from typing import Any
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from .utils import get_unique_identifier
from deliveryplus import settings
from datetime import datetime
from google.cloud import storage
from django.core.files.storage import default_storage
from google.oauth2 import service_account
import os


class ReasoneComment(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class WorkZone(models.Model):
    WORK_ZONE = [
        ("Recive", "Recive"),
        ("Storage", "Storage"),
        ("Shipment", "Shipment")
    ]

    WORKZON_ONE = 1
    WORKZON_TWO = 2
    WORKZON_THREE = 3

    WORKZON_CHOICES = (
        (WORKZON_ONE, "Recive"),
        (WORKZON_TWO, "Storage"),
        (WORKZON_THREE, "Shipment"),
    )

    name = models.CharField(max_length=10, choices=WORK_ZONE)
    way_index = models.IntegerField(choices=WORKZON_CHOICES)

    def __str__(self) -> str:
        return self.name
    
class Location(models.Model):
    name = models.CharField(max_length=20)
    work_zone = models.ForeignKey(WorkZone, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=70)
    supplier_wms_id = models.CharField(max_length = 40)

    class Meta:
        unique_together = ("name", "supplier_wms_id")
    
    def __str__(self) -> str:
        return f"{self.name} - {self.supplier_wms_id}"
    

class Shop(models.Model):
    name = models.CharField(max_length=140)
    position_nr = models.IntegerField(validators=[
            MinValueValidator(limit_value=1, message='Value must be greater than or equal to 1.'),
            MaxValueValidator(limit_value=140, message='Value must be less than or equal to 140.'),
        ])

    def __str__(self) -> str:
        return f"{self.position_nr} {self.name}"




class Delivery(models.Model):
    supplier_company = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    nr_order = models.IntegerField()# додати валідатор довжина 20 знаків
    ssc_barcode = models.CharField(max_length=20)# !!!! можливо 20 задежить чи сканер читає (00)
    images_url = models.ImageField(upload_to="images/", blank=True)
    date_recive = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField() # додати генерацію коменту
    recive_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="recive_location") # створити модель для локалізацій
    delivery_id = None # стоворити функцію для генерації унікального коду YYYY:MM:DD:NNN
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="location")
    identifier = models.IntegerField(default=get_unique_identifier(), unique=True)
    def __str__(self):
        return str(self.nr_order)



def custom_upload_path(instance, filename):
    main_path = datetime.now().strftime("%Y/%m/%d/")
    syfix_name = datetime.now().strftime("%H%M%S%f")[:-3]
    filename, file_extension = os.path.splitext(filename)
    return f"{main_path}{instance.custom_prefix}_{syfix_name}{file_extension}"


class ImageModel(models.Model):
    custom_prefix = models.CharField(max_length=50, blank=True)
    image_data = models.ImageField(upload_to=custom_upload_path)


    def __str__(self):
        return self.new_filename()  # Call the method to get the new filename

    def new_filename(self):
        return os.path.basename(self.image_data.name)
    
    def delete(self, *args, **kwargs):
        self.delete_image_from_bucket()
        super().delete(*args, **kwargs)

    def delete_image_from_bucket(self):
        bucket_name = settings.GS_BUCKET_NAME
        file_path = str(self.image_data)
        credentials = service_account.Credentials.from_service_account_file('cred.json')
        client = storage.Client(credentials=credentials)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        blob.delete()

   