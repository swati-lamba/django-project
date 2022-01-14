from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.
from django.urls import reverse

STATUS_CHOICES = {
    'New', 'Hold', 'Expired'
}


class PlantDetails(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    imagePath = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=20, blank=True)
    distance = models.IntegerField(default=0, blank=True)
    postedBy = models.CharField(max_length=40)
    updatedBy = models.CharField(max_length=40)
    datePosted = models.DateTimeField(auto_now_add=True)
    lastUpdateOn = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, default="New")
    notes = models.CharField(max_length=200, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ps:plant_details', args=[self.id])


class Comment(models.Model):
    commentText = models.CharField(max_length=200, default="")
    datePosted = models.DateTimeField(auto_now_add=True)
    lastUpdateOn = models.DateTimeField(auto_now=True)
    plant = models.ForeignKey(PlantDetails, on_delete=models.CASCADE)
    postedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    updatedBy = models.CharField(max_length=20)

    def get_user_profile(self):
        return reverse('users:profile', args=[self.postedBy])

    def get_edit_url(self):
        return  reverse("ps:edit_comment", args=[self.id])

    def get_delete_url(self):
        return  reverse("ps:delete_comment", args=[self.id])

user1 = {"username": "rick", "password": "regular", "role": "regular"}
user2 = {"username": "admin", "password": "admin", "role": "admin"}
users = []
users.append(user1)
users.append(user2)
