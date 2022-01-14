from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.urls import reverse


class UserExtraDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(default="regular", max_length=50)
    gender = models.CharField(default="unknown", max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('users:profile', args=[self.user.username])


@receiver(post_save, sender=User)
def create_user_userextradetails(sender, instance, created, **kwargs):
    if created:
        UserExtraDetails.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_userextradetails(sender, instance, **kwargs):
    instance.userextradetails.save()
