from django.db import models

# Create your models here.


class IamUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class RegisterStatus(models.TextChoices):
        CREATED = "CREATED"
        VERIFIED = "VERIFIED"  # email verified

    status = models.TextField(choices=RegisterStatus, default=RegisterStatus.CREATED)

    def __str__(self):
        return self.email
