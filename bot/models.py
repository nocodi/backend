from django.contrib.postgres.fields import ArrayField
from django.db import models


class Bot(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(default="", blank=True, null=True)
    token = models.CharField(max_length=255, unique=True, blank=False, null=False)
    user = models.ForeignKey(
        "iam.IamUser",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bot"
        verbose_name = "Bot"
        verbose_name_plural = "Bots"

    def __str__(self) -> str:
        return self.name
