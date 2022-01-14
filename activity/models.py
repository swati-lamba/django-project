from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from django.urls import reverse


class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verb = models.CharField(max_length=100)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True)


def get_target_absolute_url(self):
    if isinstance(self.target, User):
        return reverse('users:profile', args=[self.target.userextradetails.username])
    else:
        return reverse('ps:plant_details', args=[self.target.id])
