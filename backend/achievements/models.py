from django.db import models
from django.conf import settings
from django.core.validators import EmailValidator
from business.models import Business

import uuid
import qrcode
import os


ACHIEVEMENT_TYPES = (
    ("INT", "Interest"),
    ("EVENT", "Event")
)

def upload_function_qr(instance, filename):
    img_path = '/'.join([settings.QRCODE_DIR, instance.code[0:2], instance.code[2:4], instance.code[4:6], instance.code[6:8], f"{instance.code[8:10]}.jpg"])

    os.makedirs(os.path.dirname(img_path), exist_ok=True)

    return img_path

def upload_function(instance, filename):
    img_path = '/'.join([settings.IMAGES_DIR, instance.code[0:2], instance.code[2:4], instance.code[4:6], instance.code[6:8], f"{instance.code[8:10]}.jpg"])

    os.makedirs(os.path.dirname(img_path), exist_ok=True)

    return img_path

class Achievement(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    points = models.IntegerField(default=1, null=False)
    code = models.CharField(max_length=100, blank=False, null=False, unique=True)
    category = models.CharField(max_length=10, choices=ACHIEVEMENT_TYPES, default=ACHIEVEMENT_TYPES[0])
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)
    qrcode = models.ImageField(upload_to=upload_function_qr, null=False)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, null=False)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, null=False)

    description = models.TextField(null=False, max_length=512, blank=True, default="")

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if it's a new record
        if self.pk is None:
            # Generate a random code using uuid
            self.code = uuid.uuid4().hex

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.code)
            qr.make(fit=True)

            # Create an image from the QR code
            img = qr.make_image(fill_color="black", back_color="white")

            # Save the image to the specified path
            img_path = upload_function_qr(self, None)  # Pass None for filename, as it will be generated automatically
            img.save(img_path)

            # Set the qrcode field to the saved QR code image path
            self.qrcode = img_path

        super().save(*args, **kwargs)