from django.db import models



class DiscordNotification(models.Model):
    message = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Message"
    )
    image = models.ImageField(
        upload_to="discord_images/", blank=True, null=True, verbose_name="Image"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification - {self.message[:20] if self.message else 'No Message'}"


class DiscordMessage(models.Model):
    phone_number = models.CharField(max_length=15)
    message = models.TextField()
    image = models.ImageField(upload_to="discord_images/", null=True, blank=True)
    purchasing_cost = models.IntegerField(default=0, null=True, blank=True)
    express = models.CharField(max_length=50, null=True, blank=True)
    express_price = models.IntegerField(default=0)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"Message to {self.phone_number} at {self.sent_at}"
