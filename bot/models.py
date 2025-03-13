from django.db import models


class Bot(models.Model):
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    user = models.ForeignKey("iam.IamUser", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bot"
        verbose_name = "Bot"
        verbose_name_plural = "Bots"

    def __str__(self) -> str:
        return self.name
